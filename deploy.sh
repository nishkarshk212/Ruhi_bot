#!/bin/bash

# Ruhi_bot Deployment Script
# This script deploys the bot to the remote server

SERVER_IP="161.118.250.195"
SERVER_USER="root"
SSH_KEY="/tmp/ruhi_deploy_key"
REPO_URL="https://github.com/nishkarshk212/Ruhi_bot.git"
BOT_NAME="Ruhi_bot"

echo "🚀 Starting deployment to $SERVER_IP..."

# SSH options
SSH_OPTS="-i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

# Connect to server and setup
ssh $SSH_OPTS $SERVER_USER@$SERVER_IP << 'EOF'
    echo "📡 Connected to server..."
    
    # Update system packages
    echo "⚙️  Updating system packages..."
    apt update && apt upgrade -y
    
    # Install required packages
    echo "📦 Installing dependencies..."
    apt install -y python3 python3-pip git ffmpeg wget curl sudo
    
    # Create bot directory
    echo "📁 Creating bot directory..."
    mkdir -p /root/$BOT_NAME
    cd /root/$BOT_NAME
    
    # Clone repository
    echo "🔄 Cloning repository..."
    git clone $REPO_URL .
    
    # Create virtual environment
    echo "🐍 Setting up Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    # Install Python dependencies
    echo "📚 Installing Python requirements..."
    pip install --upgrade pip
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    else
        echo "⚠️  requirements.txt not found!"
        exit 1
    fi
    
    # Create .env file from example
    echo "🔧 Setting up environment configuration..."
    if [ -f Ruhi_bot.env.example ]; then
        cp Ruhi_bot.env.example .env
        echo "✅ Created .env file from template"
        echo "⚠️  IMPORTANT: Edit /root/$BOT_NAME/.env with your actual credentials!"
    else
        echo "⚠️  Ruhi_bot.env.example not found!"
    fi
    
    # Setup systemd service
    echo "🔧 Setting up systemd service..."
    cat > /etc/systemd/system/$BOT_NAME.service << 'SERVICEOF'
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
    
    # Enable and start service
    echo "🚀 Starting bot service..."
    systemctl daemon-reload
    systemctl enable $BOT_NAME
    systemctl start $BOT_NAME
    
    # Check status
    echo "📊 Checking service status..."
    systemctl status $BOT_NAME --no-pager
    
    echo ""
    echo "✅ Deployment completed successfully!"
    echo "=========================================="
    echo "Bot directory: /root/$BOT_NAME"
    echo "Service name: $BOT_NAME"
    echo ""
    echo "Useful commands:"
    echo "  systemctl status $BOT_NAME     # Check status"
    echo "  systemctl stop $BOT_NAME       # Stop bot"
    echo "  systemctl restart $BOT_NAME    # Restart bot"
    echo "  journalctl -u $BOT_NAME -f     # View logs"
    echo ""
    echo "⚠️  REMINDER: Edit /root/$BOT_NAME/.env with your actual credentials before starting!"
    echo "=========================================="
EOF

if [ $? -eq 0 ]; then
    echo "✅ Deployment script executed successfully!"
else
    echo "❌ Deployment failed!"
    exit 1
fi
