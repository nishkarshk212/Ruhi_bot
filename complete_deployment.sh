#!/bin/bash

# Complete Deployment Script for Ruhi_bot
# This script will guide you through generating session string and completing deployment

SERVER_IP="161.118.250.195"
SSH_KEY="/tmp/ruhi_deploy_key"

echo "🚀 Ruhi_bot Complete Deployment Guide"
echo "======================================"
echo ""
echo "This script will help you:"
echo "1. Generate session string"
echo "2. Configure .env file"
echo "3. Start the bot permanently"
echo ""
echo "⚠️  BEFORE YOU BEGIN, make sure you have:"
echo "   - API_ID from https://my.telegram.org"
echo "   - API_HASH from https://my.telegram.org"
echo "   - BOT_TOKEN from @BotFather"
echo "   - MONGO_DB_URI (MongoDB connection string)"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# SSH into server and generate session
echo ""
echo "📡 Connecting to server..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no root@$SERVER_IP << 'ENDSSH'
cd /root/Ruhi_bot
source venv/bin/activate

echo ""
echo "🔑 Session String Generator"
echo "==========================="
echo ""
echo "Please get your API credentials from https://my.telegram.org"
echo ""

# Run session generator
python3 << 'PYTHON_EOF'
from pyrogram import Client
from colorama import Fore, Style, init
import asyncio

init(autoreset=True)

print(Fore.CYAN + '='*50)
print(Fore.YELLOW + "  Pyrogram V2 Session String Generator")
print(Fore.CYAN + '='*50 + Style.RESET_ALL)
print()

api_id = input("Enter your API_ID: ").strip()
api_hash = input("Enter your API_HASH: ").strip()

if not api_id or not api_hash:
    print(Fore.RED + "\n❌ API_ID and API_HASH are required!" + Style.RESET_ALL)
    exit(1)

print(Fore.GREEN + "\nStarting session generation..." + Style.RESET_ALL)
print(Fore.YELLOW + "Note: You will receive a login code on your Telegram app" + Style.RESET_ALL)
print(Fore.YELLOW + "Enter the phone number with country code (e.g., +1234567890)" + Style.RESET_ALL)
print()

async def generate_session():
    async with Client(
        "session_generator",
        api_id=int(api_id),
        api_hash=api_hash,
        in_memory=True,
    ) as app:
        session_string = await app.export_session_string()
        
        print(Fore.GREEN + '\n' + '='*50 + Style.RESET_ALL)
        print(Fore.GREEN + "✅ Session Generated Successfully!" + Style.RESET_ALL)
        print(Fore.GREEN + '='*50 + Style.RESET_ALL)
        print()
        print(Fore.CYAN + "Your Session String:" + Style.RESET_ALL)
        print()
        print(Fore.WHITE + session_string + Style.RESET_ALL)
        print()
        print(Fore.GREEN + '='*50 + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "📝 IMPORTANT: Copy this session string!" + Style.RESET_ALL)
        print(Fore.YELLOW + "You'll need it for the .env file configuration." + Style.RESET_ALL)
        print()
        
        return session_string

try:
    asyncio.run(generate_session())
except Exception as e:
    print(Fore.RED + f"\n❌ Error: {str(e)}" + Style.RESET_ALL)
    exit(1)
PYTHON_EOF

echo ""
echo "✅ Session generation complete!"
echo ""
echo "Now let's configure the .env file..."
echo ""
echo "Please provide the following information:"
echo ""

# Get API credentials
read -p "Enter API_ID: " api_id
read -p "Enter API_HASH: " api_hash
read -p "Enter BOT_TOKEN: " bot_token
read -p "Enter OWNER_ID (your Telegram user ID): " owner_id
read -p "Enter STRING_SESSION (paste the generated session): " string_session
read -p "Enter MONGO_DB_URI: " mongo_uri
read -p "Enter LOGGER_ID (channel ID, optional, press Enter to skip): " logger_id

# Set defaults if empty
logger_id=${logger_id:--100}

# Create .env file
cat > .env << EOF
# Ruhi_bot Configuration
API_ID=$api_id
API_HASH=$api_hash
BOT_TOKEN=$bot_token
MONGO_DB_URI=$mongo_uri
OWNER_ID=$owner_id
LOGGER_ID=$logger_id
STRING_SESSION=$string_session

# Optional APIs (leave empty if not needed)
DEEP_API=
GPT_API=
OPENAI_API_KEY=
JOKE_API_URL=
STRIPE_API_KEY=
NEXGENBOTS_API=https://pvtz.nexgenbots.xyz
VIDEO_API_URL=https://pvtz.nexgenbots.xyz
API_KEY=
EOF

echo ""
echo "✅ .env file created successfully!"
echo ""
echo "🔧 Configuring systemd service..."

# Create systemd service
cat > /etc/systemd/system/Ruhi_bot.service << 'SERVICEOF'
[Unit]
Description=Ruhi_bot Telegram Music Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Ruhi_bot
Environment="PATH=/root/Ruhi_bot/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/root/Ruhi_bot/venv/bin/python3 -m ANNIEMUSIC
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEOF

# Reload and start service
systemctl daemon-reload
systemctl enable Ruhi_bot
systemctl restart Ruhi_bot

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Checking bot status..."
sleep 3
systemctl status Ruhi_bot --no-pager

echo ""
echo "=========================================="
echo "✅ Ruhi_bot is now running permanently!"
echo "=========================================="
echo ""
echo "Useful commands:"
echo "  systemctl status Ruhi_bot     # Check status"
echo "  systemctl stop Ruhi_bot       # Stop bot"
echo "  systemctl restart Ruhi_bot    # Restart bot"
echo "  journalctl -u Ruhi_bot -f     # View logs"
echo ""
ENDSSH

echo ""
echo "🎉 All done! Your bot should be running now."
echo ""
