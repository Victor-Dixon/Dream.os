# Discord Bot Setup Instructions

## Step 1: Create Discord Application
1. Go to https://discord.com/developers/applications
2. Click 'New Application'
3. Name it 'Dream.os Agent Controller'
4. Go to 'Bot' section
5. Click 'Add Bot'

## Step 2: Get Bot Token
1. In Bot section, click 'Copy' under Token
2. This token goes in your .env file as DISCORD_BOT_TOKEN

## Step 3: Bot Permissions
1. Go to 'General Information' section
2. Copy 'Application ID'
3. Use this URL to invite bot:
   https://discord.com/api/oauth2/authorize?client_id=YOUR_APP_ID&permissions=414464658496&scope=bot

## Step 4: Configure Dream.os
Edit .env file and set:
DISCORD_BOT_TOKEN=your_token_here

## Step 5: Start Discord Service
python main.py --discord --background
