# Twitch Channel Points Integration Setup

## Overview

This system allows Twitch viewers to spend channel points to interact with the agent swarm system. Viewers can issue directives, vote on tasks, inject constraints, and more.

## Architecture

1. **Channel Points Rewards Config** (`channel_points_rewards.py`)
   - Defines available rewards
   - Maps rewards to handler functions
   - Handles rate limiting and approval workflows

2. **EventSub Webhook Handler** (`twitch_eventsub_handler.py`)
   - Receives Twitch EventSub webhook notifications
   - Verifies webhook signatures
   - Routes redemptions to reward handlers

3. **Reward Handlers**
   - Execute agent swarm actions via `messaging_cli`
   - Return response messages for chat

## Setup Steps

### 1. Create Channel Point Rewards on Twitch

1. Go to your Twitch Creator Dashboard
2. Navigate to **Channel Points** → **Custom Rewards**
3. Create each reward with these exact names:

#### MVP Rewards

| Reward Name | Points Cost | Description |
|------------|-------------|-------------|
| **Force Agent Status Report** | 100 | Issue a Swarm Directive: Force an agent to provide live status |
| **Vote on Next Task** | 50 | Influence task prioritization |
| **Inject Constraint** | 75 | Add creative constraint to next agent task |
| **Name in Devlog** | 200 | Get credited in next devlog publication |
| **Chaos Mode** | 150 | Trigger random constraint mode for agent |
| **Explain Reasoning** | 100 | Break down last agent decision |
| **Unlock Operator Title** | 500 | Earn 'Junior Operator' swarm title |

**Important Settings:**
- ✅ **Enable "Require Viewer Input"** for rewards that need context
- ✅ Set **"Redemptions per Stream"** limits if desired
- ⚠️ Set **"Global Cooldown"** matching rate limits in config
- 🔒 **"Require Approval"** optional (future feature)

### 2. Set Up EventSub Webhook Subscription

You need to create an EventSub webhook subscription via Twitch API.

#### Option A: Use Twitch CLI (Recommended for Testing)

```bash
# Install Twitch CLI: https://dev.twitch.tv/docs/cli/

# Authenticate
twitch token

# Subscribe to channel point redemptions
twitch event subscribe channel.channel_points_custom_reward_redemption.add \
  --condition broadcaster_user_id=YOUR_TWITCH_USER_ID \
  --transport webhook \
  --secret YOUR_WEBHOOK_SECRET \
  --url https://your-domain.com/twitch/eventsub
```

#### Option B: Use Twitch API Directly

See: https://dev.twitch.tv/docs/eventsub/manage-subscriptions/

### 3. Configure Webhook Secret

Set environment variable:

```bash
export TWITCH_EVENTSUB_WEBHOOK_SECRET="your-webhook-secret-here"
```

Or add to `.env`:

```
TWITCH_EVENTSUB_WEBHOOK_SECRET=your-webhook-secret-here
```

### 4. Run Webhook Server

```bash
python -m src.services.chat_presence.twitch_eventsub_server
```

Or integrate into existing Flask app:

```python
from src.services.chat_presence.twitch_eventsub_handler import create_eventsub_flask_app
import os

app = create_eventsub_flask_app(
    webhook_secret=os.getenv("TWITCH_EVENTSUB_WEBHOOK_SECRET"),
    on_redemption=lambda user, data: print(f"{user} redeemed reward")
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### 5. Map Reward IDs (Optional)

After creating rewards on Twitch, you can get their IDs and update `channel_points_rewards.py`:

```python
# Find reward ID via Twitch API or EventSub payload logs
MVP_REWARDS["force_status_report"].reward_id = "abc123-def456-..."
```

Or match by name (current default) - the handler will match rewards by title.

## Testing

1. **Webhook Verification**: Twitch will send a verification challenge. The handler should respond with the challenge value.

2. **Test Redemption**: 
   - Redeem a reward on Twitch
   - Check webhook logs for processing
   - Verify agent message was sent
   - Check chat for response message

## Reward Handler Customization

Each reward handler function receives:

- `user_name`: Twitch username
- `user_id`: Twitch user ID  
- `redemption_id`: Unique redemption ID
- `reward_data`: Dict with reward info and user input

Handler should return a string message for chat response.

Example handler:

```python
def handle_custom_reward(
    user_name: str,
    user_id: str,
    redemption_id: str,
    reward_data: Dict[str, Any]
) -> str:
    """Custom reward handler."""
    import subprocess
    
    # Execute agent action
    subprocess.run([
        "python", "-m", "src.services.messaging_cli",
        "--agent", "Agent-4",
        "--message", f"Custom action from {user_name}",
        "--type", "text",
        "--category", "a2c"
    ])
    
    return f"✅ Custom action executed by {user_name}!"
```

## Future Enhancements

- [ ] Approval queue for high-impact rewards
- [ ] Viewer voting system with vote accumulation
- [ ] Swarm rank/XP tracking system
- [ ] Reward cooldown per viewer (not just global)
- [ ] Reward history and analytics
- [ ] Integration with Discord bot for responses

## Troubleshooting

**Webhook not receiving events:**
- Verify webhook URL is publicly accessible (use ngrok for local dev)
- Check Twitch EventSub subscription status
- Verify webhook secret matches

**Rewards not matching:**
- Check reward name matches exactly (case-sensitive)
- Check reward_id if set
- Look for warning logs about unknown rewards

**Rate limiting issues:**
- Adjust `rate_limit_seconds` in reward config
- Check `last_redemptions` tracking

**Agent messages not sending:**
- Verify `messaging_cli` is working
- Check agent IDs are correct
- Review subprocess error logs

