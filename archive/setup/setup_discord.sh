#!/bin/bash
# Dream.os Discord Bot Setup Script

echo "🐝 Dream.os Discord Bot Setup"
echo "=============================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run install.sh first."
    exit 1
fi

# Check if token is already set
if grep -q "DISCORD_BOT_TOKEN=.*[a-zA-Z0-9]" .env; then
    echo "✅ Discord bot token appears to be configured"
else
    echo "⚠️  Discord bot token not found in .env"
    echo ""
    echo "To set up Discord bot integration:"
    echo "1. Go to https://discord.com/developers/applications"
    echo "2. Create a new application named 'Dream.os'"
    echo "3. Go to Bot section and create a bot"
    echo "4. Copy the bot token"
    echo "5. Add this line to your .env file:"
    echo "   DISCORD_BOT_TOKEN=your_token_here"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "🔧 Testing Discord bot configuration..."

# Test token format
source venv/bin/activate
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('DISCORD_BOT_TOKEN')
if not token:
    print('❌ DISCORD_BOT_TOKEN not found')
    exit(1)
elif len(token) < 50:
    print('❌ DISCORD_BOT_TOKEN appears too short')
    exit(1)
elif not token.startswith('M') and not token.startswith('N') and not token.startswith('O'):
    print('⚠️  DISCORD_BOT_TOKEN format looks unusual (should start with M, N, or O)')
else:
    print('✅ DISCORD_BOT_TOKEN format looks correct')
"

echo ""
echo "🚀 Starting Discord bot service..."
echo "Run this command in another terminal:"
echo "  python main.py --discord --background"
echo ""
echo "Or start it now (will run in background):"
read -p "Start Discord service now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    source venv/bin/activate
    python main.py --discord --background
    echo "✅ Discord service started in background"
    echo "Check status with: python main.py --status"
fi
