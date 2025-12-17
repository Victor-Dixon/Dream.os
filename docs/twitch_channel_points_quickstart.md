# Twitch Channel Points - Quick Start

## ✅ What Was Built

A complete system for Twitch viewers to spend channel points to control the agent swarm:

- **7 MVP Rewards** ready to use
- **EventSub webhook handler** with signature verification
- **Rate limiting** to prevent abuse
- **Integration with messaging_cli** (SSOT compliant)
- **Complete documentation**

## 🚀 Quick Setup (3 Steps)

### 1. Install Flask

```bash
pip install flask
```

### 2. Create Rewards on Twitch

Go to Creator Dashboard → Channel Points → Custom Rewards

Create these exact rewards:
- **Force Agent Status Report** (100 points)
- **Vote on Next Task** (50 points)
- **Inject Constraint** (75 points)
- **Name in Devlog** (200 points)
- **Chaos Mode** (150 points)
- **Explain Reasoning** (100 points)
- **Unlock Operator Title** (500 points)

### 3. Run Webhook Server

```bash
export TWITCH_EVENTSUB_WEBHOOK_SECRET="your-webhook-secret"
python -m src.services.chat_presence.twitch_eventsub_server
```

Then subscribe to EventSub via Twitch API/CLI.

## 📚 Full Documentation

See `docs/twitch_channel_points_setup.md` for complete setup guide.

## 🎯 How It Works

1. Viewer redeems reward → Twitch sends webhook
2. Handler verifies signature → Security check
3. Reward handler executes → Sends agent message via `messaging_cli`
4. Response returned → Can post to chat

All rewards use the canonical messaging system - no ad-hoc scripts! ✅

