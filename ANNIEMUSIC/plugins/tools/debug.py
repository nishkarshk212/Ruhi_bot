from pyrogram import filters
from ANNIEMUSIC import app

@app.on_message(filters.command("testbot"))
async def test_bot_respond(client, message):
    await message.reply_text("I am alive and responding!")

@app.on_message(filters.all, group=10)
async def log_all_messages(client, message):
    print(f"DEBUG: Received message from {message.from_user.id if message.from_user else 'Unknown'} in {message.chat.id}: {message.text or message.caption or 'Media'}")
