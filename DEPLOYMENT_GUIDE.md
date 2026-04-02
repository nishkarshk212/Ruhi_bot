# 🚀 Ruhi_bot Complete Deployment Guide

## ✅ What's Already Done

Your server at `161.118.250.195` is fully prepared:
- ✅ All dependencies installed
- ✅ Bot codebase cloned
- ✅ Python virtual environment created
- ✅ Systemd service configured
- ⏳ Waiting for configuration (session string + credentials)

---

## 🔑 Step-by-Step Configuration

### Step 1: Get Your Telegram API Credentials

1. Go to https://my.telegram.org
2. Login with your phone number (the one you want associated with the bot)
3. Click on "API development tools"
4. Create a new application:
   - **App name**: Ruhi_bot
   - **Short description**: Music bot
   - **Platform**: Other
5. Copy your **API_ID** and **API_HASH**

### Step 2: Get Bot Token

1. Open Telegram and search for @BotFather
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the **BOT_TOKEN**

### Step 3: Connect to Server and Generate Session

Execute these commands on your local machine:

```bash
# SSH into the server
ssh -i /tmp/ruhi_deploy_key root@161.118.250.195

# Navigate to bot directory
cd /root/Ruhi_bot

# Activate virtual environment
source venv/bin/activate

# Run session generator
python3 generate_session.py
```

The script will ask for:
- **API_ID**: Enter the one you got from Step 1
- **API_HASH**: Enter the one you got from Step 1

Then it will ask for your phone number. Enter it with country code (e.g., `+1234567890`)

You'll receive a login code on your Telegram app. Enter it when prompted.

After successful login, you'll get a **SESSION_STRING**. Copy it!

### Step 4: Configure .env File

While still connected to the server, run:

```bash
nano .env
```

Replace the placeholder values with your actual credentials:

```env
# Required Configuration
API_ID=12345678                    # Replace with your actual API_ID
API_HASH=your_actual_api_hash      # Replace with your actual API_HASH
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz  # Replace with your bot token
MONGO_DB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority  # Your MongoDB URI
OWNER_ID=123456789                 # Your Telegram user ID (get from @userinfobot)
LOGGER_ID=-1001234567890           # Channel ID or keep as -100
STRING_SESSION=BQI...              # Paste the session string you generated

# Optional (leave empty if not needed)
DEEP_API=
GPT_API=
OPENAI_API_KEY=
JOKE_API_URL=
STRIPE_API_KEY=
NEXGENBOTS_API=https://pvtz.nexgenbots.xyz
VIDEO_API_URL=https://pvtz.nexgenbots.xyz
API_KEY=
```

To save in nano:
- Press `Ctrl + X`
- Press `Y`
- Press `Enter`

### Step 5: Start the Bot

```bash
# Reload systemd to pick up any changes
systemctl daemon-reload

# Enable the bot to start on boot
systemctl enable Ruhi_bot

# Start the bot
systemctl start Ruhi_bot

# Check status
systemctl status Ruhi_bot
```

If you see `Active: active (running)`, congratulations! Your bot is running! 🎉

---

## 🔍 Useful Commands

### Check if bot is running:
```bash
systemctl status Ruhi_bot
```

### View live logs:
```bash
journalctl -u Ruhi_bot -f
```

### Restart bot:
```bash
systemctl restart Ruhi_bot
```

### Stop bot:
```bash
systemctl stop Ruhi_bot
```

### Start bot:
```bash
systemctl start Ruhi_bot
```

### View all logs since boot:
```bash
journalctl -u Ruhi_bot --since boot
```

---

## 📝 Quick Reference

### Server Details:
- **IP**: 161.118.250.195
- **Username**: root
- **SSH Key**: /tmp/ruhi_deploy_key
- **Bot Directory**: /root/Ruhi_bot
- **Virtual Env**: /root/Ruhi_bot/venv
- **Service Name**: Ruhi_bot

### Get Help:
```bash
# SSH to server
ssh -i /tmp/ruhi_deploy_key root@161.118.250.195

# Check bot status
systemctl status Ruhi_bot

# View logs
journalctl -u Ruhi_bot -n 50
```

---

## ❓ Troubleshooting

### Bot won't start?
Check the logs:
```bash
journalctl -u Ruhi_bot -n 100
```

Common issues:
1. **Invalid API credentials**: Double-check API_ID and API_HASH
2. **Invalid BOT_TOKEN**: Make sure you copied the complete token
3. **Invalid MONGO_DB_URI**: Verify your MongoDB connection string
4. **Missing STRING_SESSION**: Generate and add the session string

### Need to regenerate session string?
```bash
cd /root/Ruhi_bot
source venv/bin/activate
python3 generate_session.py
```

### Bot crashes on startup?
Check the error logs and verify all credentials in `.env` are correct.

---

## 🎉 Success!

Once your bot is running, you can test it by searching for it on Telegram and sending `/start`.

Your bot will now:
- ✅ Start automatically on server reboot
- ✅ Restart automatically if it crashes
- ✅ Run 24/7 permanently

---

**Deployment completed!** 🚀
