"""
Auto Maintenance Module - Auto restart, update, and cache cleanup
Runs every 24 hours to keep the bot fresh and clean
"""

import asyncio
import os
import shutil
import subprocess
from datetime import datetime
from ANNIEMUSIC import app
from pyrogram import filters
from ANNIEMUSIC.utils.database import is_served_user
from config import OWNER_ID

# Schedule interval (24 hours in seconds)
MAINTENANCE_INTERVAL = 24 * 60 * 60  # 86400 seconds

async def clear_cache():
    """Clear unnecessary cache and temporary files"""
    try:
        # Directories to clean
        cache_dirs = [
            "cache",
            "downloads",
            "__pycache__",
            "ANNIEMUSIC/__pycache__",
            "ANNIEMUSIC/core/__pycache__",
            "ANNIEMUSIC/mongo/__pycache__",
            "ANNIEMUSIC/platforms/__pycache__",
            "ANNIEMUSIC/plugins/__pycache__",
            "ANNIEMUSIC/utils/__pycache__",
            "ANNIEMUSIC/utils/decorators/__pycache__",
            "ANNIEMUSIC/utils/inline/__pycache__",
            "ANNIEMUSIC/utils/stream/__pycache__",
            "ANNIEMUSIC/plugins/Kishu/__pycache__",
            "ANNIEMUSIC/plugins/admins/__pycache__",
            "ANNIEMUSIC/plugins/bot/__pycache__",
            "ANNIEMUSIC/plugins/misc/__pycache__",
            "ANNIEMUSIC/plugins/play/__pycache__",
            "ANNIEMUSIC/plugins/sudo/__pycache__",
            "ANNIEMUSIC/plugins/tools/__pycache__",
            "strings/__pycache__",
        ]
        
        cleaned_count = 0
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                for file in os.listdir(cache_dir):
                    if file.endswith(('.pyc', '.pyo', '__pycache__')):
                        file_path = os.path.join(cache_dir, file)
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                                cleaned_count += 1
                        except Exception:
                            pass
        
        # Clear old downloads (older than 24 hours)
        if os.path.exists("downloads"):
            for file in os.listdir("downloads"):
                file_path = os.path.join("downloads", file)
                try:
                    if os.path.isfile(file_path):
                        # Check file age
                        file_age = datetime.now().timestamp() - os.path.getmtime(file_path)
                        if file_age > MAINTENANCE_INTERVAL:
                            os.remove(file_path)
                            cleaned_count += 1
                except Exception:
                    pass
        
        # Clear old cache files
        if os.path.exists("cache"):
            for file in os.listdir("cache"):
                file_path = os.path.join("cache", file)
                try:
                    if os.path.isfile(file_path):
                        # Check file age
                        file_age = datetime.now().timestamp() - os.path.getmtime(file_path)
                        if file_age > MAINTENANCE_INTERVAL:
                            os.remove(file_path)
                            cleaned_count += 1
                except Exception:
                    pass
        
        return cleaned_count
    except Exception as e:
        print(f"Error clearing cache: {e}")
        return 0

async def auto_update():
    """Pull latest updates from git repository"""
    try:
        # Check if .git directory exists
        if not os.path.exists(".git"):
            return False, "Not a git repository"
        
        # Fetch updates
        subprocess.run(["git", "fetch", "--all"], check=True, capture_output=True)
        
        # Check for updates
        result = subprocess.run(
            ["git", "status", "-uno"],
            check=True,
            capture_output=True,
            text=True
        )
        
        if "Your branch is behind" in result.stdout:
            # Pull updates
            subprocess.run(["git", "pull", "--force"], check=True, capture_output=True)
            return True, "Updates pulled successfully"
        else:
            return False, "Already up to date"
    except Exception as e:
        return False, f"Update failed: {str(e)}"

async def perform_maintenance():
    """Perform all maintenance tasks"""
    try:
        print("=" * 50)
        print("🔧 Starting Scheduled Maintenance...")
        print("=" * 50)
        
        # 1. Clear cache and unnecessary files
        print("🗑️  Clearing cache and temporary files...")
        cleaned_count = await clear_cache()
        print(f"✅ Cleaned {cleaned_count} unnecessary files")
        
        # 2. Check and apply updates
        print("📥 Checking for updates...")
        updated, message = await auto_update()
        if updated:
            print(f"✅ {message}")
        else:
            print(f"ℹ️  {message}")
        
        # 3. Restart the bot
        print("🔄 Restarting bot service...")
        
        # Send notification to owner if bot is running
        try:
            await app.send_message(
                OWNER_ID,
                f"🔧 **Maintenance Completed**\n\n"
                f"🗑️ Cleaned: {cleaned_count} files\n"
                f"📥 Updates: {message}\n"
                f"🔄 Status: Restarting now..."
            )
        except Exception:
            pass
        
        # Graceful restart using systemd
        os.system("systemctl restart Ruhi_bot")
        
        print("=" * 50)
        print("✅ Maintenance completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Maintenance error: {e}")
        # Try simple restart as fallback
        os.system("systemctl restart Ruhi_bot")

# Background task for scheduled maintenance
async def maintenance_scheduler():
    """Run maintenance every 24 hours"""
    while True:
        try:
            # Wait until next scheduled time (24 hours)
            await asyncio.sleep(MAINTENANCE_INTERVAL)
            
            # Perform maintenance
            await perform_maintenance()
            
        except Exception as e:
            print(f"Scheduler error: {e}")
            # Continue even if there's an error
            continue

# Manual trigger command for testing
@app.on_message(filters.command("maintain") & filters.user(OWNER_ID))
async def manual_maintenance(client, message):
    """Manually trigger maintenance (Owner only)"""
    try:
        msg = await message.reply("🔧 Starting maintenance...")
        
        # Clear cache
        cleaned_count = await clear_cache()
        await msg.edit_text(f"🗑️ Cleaned {cleaned_count} files\n\n🔄 Use /restart to restart the bot")
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

# Start the maintenance scheduler when bot starts
async def start_maintenance_scheduler():
    """Initialize the maintenance scheduler"""
    print("⏰ Starting 24-hour maintenance scheduler...")
    asyncio.create_task(maintenance_scheduler())
    print("✅ Maintenance scheduler started")
