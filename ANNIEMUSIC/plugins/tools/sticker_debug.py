"""
Sticker Debug Plugin - Logs all sticker details
Send any sticker to the bot in private message to see its details
"""

from pyrogram import filters, enums
from pyrogram.types import Message
from ANNIEMUSIC import app
import logging

# Set up logging
logger = logging.getLogger(__name__)

@app.on_message(filters.private & filters.sticker)
async def sticker_debug_handler(client, message: Message):
    """Debug handler to log all sticker details in private messages"""
    
    sticker = message.sticker
    
    # Build detailed information message
    info_text = f"""
🎨 **STICKER DETAILS** 🎨

📋 **Basic Info:**
• File ID: `{sticker.file_id}`
• Unique ID: `{sticker.file_unique_id}`
• Set Name: `{sticker.set_name or 'N/A'}`

🎭 **Type:**
• Static: {sticker.is_animated == False and sticker.is_video == False}
• Animated: {sticker.is_animated}
• Video: {sticker.is_video}

📏 **Dimensions:**
• Width: {sticker.width}px
• Height: {sticker.height}px
• File Size: {sticker.file_size or 0} bytes

🎬 **Premium/Custom Emoji Info:**
• Is Premium: {sticker.premium_animation is not None}
• Custom Emoji: {sticker.is_premium_animation if hasattr(sticker, 'is_premium_animation') else 'N/A'}

✨ **Emoji:**
• Associated Emoji: `{sticker.emoji or 'N/A'}`

📦 **Set Info:**
• Sticker Set: {sticker.set_name or 'Not in set'}

🔍 **Type Number:**
• Type: {sticker.type}
"""
    
    # Send info to user
    await message.reply_text(info_text, parse_mode=enums.ParseMode.MARKDOWN)
    
    # Log to console
    logger.info(f"📱 STICKER RECEIVED in PM from {message.from_user.id} ({message.from_user.username})")
    logger.info(f"File ID: {sticker.file_id}")
    logger.info(f"Type: Animated={sticker.is_animated}, Video={sticker.is_video}")
    logger.info(f"Premium: {sticker.premium_animation is not None}")
    logger.info(f"Emoji: {sticker.emoji}")
    logger.info(f"Set: {sticker.set_name}")
    
    # Also forward the sticker back with info
    try:
        await message.reply_sticker(sticker.file_id)
        await message.reply_text("✅ Sticker sent back! Check the info above for details.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error sending sticker back: {str(e)}")


@app.on_message(filters.command("mystickers"))
async def list_my_stickers(client, message: Message):
    """Show how to get sticker information"""
    await message.reply_text(
        "📌 **How to Check Sticker Details:**\n\n"
        "1️⃣ Send me any sticker in private message\n"
        "2️⃣ I'll show you all the details including:\n"
        "   • File ID (to reuse the sticker)\n"
        "   • Type (static/animated/video)\n"
        "   • Premium status\n"
        "   • Associated emoji\n"
        "   • Sticker set name\n\n"
        "💡 **Tip:** Copy the File ID to use this sticker in bot messages!\n\n"
        "**Example usage in code:**\n"
        "`await message.reply_sticker('YOUR_FILE_ID_HERE')`"
    )


# Also log when bot sends stickers
@app.on_message(filters.command("logs"))
async def check_logs(client, message: Message):
    """Check recent bot logs"""
    await message.reply_text(
        "📋 **To check server logs:**\n\n"
        "1. SSH into server:\n"
        "```bash\n"
        "ssh root@161.118.250.195\n"
        "```\n\n"
        "2. View recent logs:\n"
        "```bash\n"
        "tail -f /root/Ruhi_bot/bot.log\n"
        "```\n\n"
        "3. Or use systemctl:\n"
        "```bash\n"
        "journalctl -u Ruhi_bot -f\n"
        "```"
    )
