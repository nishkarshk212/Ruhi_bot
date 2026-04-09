from ANNIEMUSIC import app
from config import OWNER_ID
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ANNIEMUSIC.utils.jarvis_ban import admin_filter
from ANNIEMUSIC.misc import SUDOERS

# BOT_ID will be set when the app starts
BOT_ID = None

@app.on_message(filters.command("allban") & SUDOERS)
async def ban_all(_, msg):
    global BOT_ID
    if BOT_ID is None:
        BOT_ID = app.me.id if app.me else None
        if BOT_ID is None:
            return await msg.reply_text("❌ Bot not initialized properly.")
    
    chat_id = msg.chat.id    
    bot = await app.get_chat_member(chat_id, BOT_ID)
    bot_permission = bot.privileges.can_restrict_members == True    
    if bot_permission:
        async for member in app.get_chat_members(chat_id):       
            try:
                await app.ban_chat_member(chat_id, member.user.id)
                await msg.reply_text(f"**‣ ᴏɴᴇ ᴍᴏʀᴇ ʙᴀɴɴᴇᴅ.**\n\n➻ {member.user.mention}")                    
            except Exception:
                pass
