import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

from ANNIEMUSIC import app
from ANNIEMUSIC.misc import SUDOERS
from ANNIEMUSIC.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from ANNIEMUSIC.utils.decorators.language import language
from ANNIEMUSIC.utils.formatters import alpha_to_int
from config import adminlist

IS_BROADCASTING = False

# Dictionary to store broadcast configuration
BROADCAST_DATA = {}

def get_broadcast_menu():
    buttons = [
        [
            InlineKeyboardButton("Set Media", callback_data="broadcast_set_media"),
            InlineKeyboardButton("Set Text", callback_data="broadcast_set_text"),
        ],
        [
            InlineKeyboardButton("Set Button", callback_data="broadcast_set_button"),
        ],
        [
            InlineKeyboardButton("Broadcast", callback_data="broadcast_start"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


@app.on_message(filters.command("broadcast") & SUDOERS)
@language
async def braodcast_message(client, message, _):
    # If no arguments and not a reply, show the menu
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text(
            "**Broadcast Configuration Menu**\n\nConfigure your broadcast message using the buttons below.\n\n"
            f"**Current Config:**\n"
            f"Media: {'Set' if message.from_user.id in BROADCAST_DATA and BROADCAST_DATA[message.from_user.id].get('media') else 'Not Set'}\n"
            f"Text: {'Set' if message.from_user.id in BROADCAST_DATA and BROADCAST_DATA[message.from_user.id].get('text') else 'Not Set'}\n"
            f"Button: {'Set' if message.from_user.id in BROADCAST_DATA and BROADCAST_DATA[message.from_user.id].get('buttons') else 'Not Set'}",
            reply_markup=get_broadcast_menu()
        )

    global IS_BROADCASTING
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["broad_2"])
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-assistant" in query:
            query = query.replace("-assistant", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if "-button" in query:
            query = query.replace("-button", "")
        if query == "":
            return await message.reply_text(_["broad_8"])

    IS_BROADCASTING = True
    await message.reply_text(_["broad_1"])

    # Parse buttons from the message if -button flag is used
    reply_markup = None
    if "-button" in message.text and not message.reply_to_message:
        query, reply_markup = parse_buttons(query)

    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = (
                    await app.copy_message(i, y, x, reply_markup=reply_markup)
                    if message.reply_to_message
                    else await app.send_message(i, text=query, reply_markup=reply_markup)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        continue
                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                continue
        try:
            await message.reply_text(_["broad_3"].format(sent, pin))
        except:
            pass

    if "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_served_users()
        for user in susers:
            served_users.append(int(user["user_id"]))
        for i in served_users:
            try:
                m = (
                    await app.copy_message(i, y, x, reply_markup=reply_markup)
                    if message.reply_to_message
                    else await app.send_message(i, text=query, reply_markup=reply_markup)
                )
                susr += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                pass
        try:
            await message.reply_text(_["broad_4"].format(susr))
        except:
            pass

    if "-assistant" in message.text:
        aw = await message.reply_text(_["broad_5"])
        text = _["broad_6"]
        from ANNIEMUSIC.core.userbot import assistants

        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                try:
                    await client.copy_message(
                        dialog.chat.id, y, x, reply_markup=reply_markup
                    ) if message.reply_to_message else await client.send_message(
                        dialog.chat.id, text=query, reply_markup=reply_markup
                    )
                    sent += 1
                    await asyncio.sleep(3)
                except FloodWait as fw:
                    flood_time = int(fw.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except:
                    continue
            text += _["broad_7"].format(num, sent)
        try:
            await aw.edit_text(text)
        except:
            pass
    IS_BROADCASTING = False


@app.on_callback_query(filters.regex("^broadcast_") & SUDOERS)
async def broadcast_callbacks(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    if data == "broadcast_set_media":
        BROADCAST_DATA[user_id] = BROADCAST_DATA.get(user_id, {})
        BROADCAST_DATA[user_id]["state"] = "awaiting_media"
        await callback_query.message.edit_text(
            "Please send the media (Photo, Video, etc.) you want to broadcast.\nReply /cancel to cancel."
        )
    elif data == "broadcast_set_text":
        BROADCAST_DATA[user_id] = BROADCAST_DATA.get(user_id, {})
        BROADCAST_DATA[user_id]["state"] = "awaiting_text"
        await callback_query.message.edit_text(
            "Please send the text you want to broadcast.\nReply /cancel to cancel."
        )
    elif data == "broadcast_set_button":
        BROADCAST_DATA[user_id] = BROADCAST_DATA.get(user_id, {})
        BROADCAST_DATA[user_id]["state"] = "awaiting_button"
        await callback_query.message.edit_text(
            "Please send the buttons in one of these formats:\n\n"
            "**1. Simple Format (Recommended):**\n"
            "`Button Text | https://t.me/link` (One button per row)\n"
            "`Btn1 | link1 | Btn2 | link2` (Multiple buttons per row)\n\n"
            "**2. Advanced Format:**\n"
            "`[Text](url:https://t.me/link)`\n"
            "`[Text](callback:data)`\n\n"
            "Reply /cancel to cancel."
        )
    elif data == "broadcast_start":
        user_data = BROADCAST_DATA.get(user_id, {})
        media = user_data.get("media")
        text = user_data.get("text")
        buttons = user_data.get("buttons")
        
        if not media and not text:
            return await callback_query.answer("Please set at least media or text to broadcast.", show_alert=True)
        
        await callback_query.message.edit_text("Broadcasting started...")
        
        # Broadcasting logic
        schats = await get_served_chats()
        susers = await get_served_users()
        
        sent_chats = 0
        sent_users = 0
        
        # Combine all targets
        targets = []
        for chat in schats:
            targets.append(int(chat["chat_id"]))
        for user in susers:
            targets.append(int(user["user_id"]))
            
        for i in targets:
            try:
                if media:
                    # Forward the stored media message
                    await media.copy(i, caption=text, reply_markup=buttons)
                else:
                    await app.send_message(i, text=text, reply_markup=buttons)
                
                if i < 0: sent_chats += 1
                else: sent_users += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                await asyncio.sleep(int(fw.value))
            except:
                continue
        
        await callback_query.message.reply_text(f"Broadcast completed!\n\nSent to {sent_chats} chats and {sent_users} users.")
        # Clear data after broadcast
        BROADCAST_DATA[user_id] = {}


@app.on_message(filters.command("settext") & SUDOERS)
async def set_broadcast_text(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Please reply to a message to set its text as the broadcast text.")
    
    if not message.reply_to_message.text and not message.reply_to_message.caption:
        return await message.reply_text("The replied message doesn't have any text or caption.")
    
    text = message.reply_to_message.text or message.reply_to_message.caption
    user_id = message.from_user.id
    
    BROADCAST_DATA[user_id] = BROADCAST_DATA.get(user_id, {})
    BROADCAST_DATA[user_id]["text"] = text
    BROADCAST_DATA[user_id]["state"] = None
    
    await message.reply_text(
        "**Broadcast text has been set successfully!**\n\n"
        f"**Text:** {text[:100]}{'...' if len(text) > 100 else ''}",
        reply_markup=get_broadcast_menu()
    )


@app.on_message(SUDOERS & ~filters.command(["broadcast", "start", "help", "settext"]))
async def broadcast_input_handler(client, message: Message):
    user_id = message.from_user.id
    if user_id not in BROADCAST_DATA or not BROADCAST_DATA[user_id].get("state"):
        return
    
    if message.text == "/cancel":
        BROADCAST_DATA[user_id]["state"] = None
        return await message.reply_text("Broadcast configuration cancelled.", reply_markup=get_broadcast_menu())

    state = BROADCAST_DATA[user_id]["state"]
    
    if state == "awaiting_media":
        if message.photo or message.video or message.document or message.audio or message.animation:
            BROADCAST_DATA[user_id]["media"] = message
            BROADCAST_DATA[user_id]["state"] = None
            await message.reply_text("Media set successfully!", reply_markup=get_broadcast_menu())
        else:
            await message.reply_text("Please send valid media (Photo, Video, Document, etc.).")
            
    elif state == "awaiting_text":
        if message.text:
            BROADCAST_DATA[user_id]["text"] = message.text
            BROADCAST_DATA[user_id]["state"] = None
            await message.reply_text("Text set successfully!", reply_markup=get_broadcast_menu())
        else:
            await message.reply_text("Please send text.")
            
    elif state == "awaiting_button":
        if message.text:
            _, reply_markup = parse_buttons(message.text)
            if reply_markup:
                BROADCAST_DATA[user_id]["buttons"] = reply_markup
                BROADCAST_DATA[user_id]["state"] = None
                await message.reply_text("Buttons set successfully!", reply_markup=get_broadcast_menu())
            else:
                await message.reply_text("Invalid button format. Please use `[Text](url:URL)`.")
        else:
            await message.reply_text("Please send button text.")



def parse_buttons(text):
    """
    Parse buttons from text.
    Supported formats:
    1. Simple: Button Text | URL
    2. Multiple in row: Button 1 | URL1 | Button 2 | URL2
    3. Markdown: [Text](url:URL) or [Text](callback:DATA)
    """
    import re
    
    # Regex for markdown format
    md_button_pattern = r'\[([^\]]+)\]\((url|callback):([^\)]+)\)'
    # Regex for simple format: Any text | Any URL (starting with http)
    simple_button_pattern = r'(.+?)\s*\|\s*(https?://[^\s|]+)'
    
    buttons = []
    lines = text.split('\n')
    clean_text = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        row = []
        # First check for markdown style
        if re.search(md_button_pattern, line):
            # Check if multiple markdown buttons in same row (separated by |)
            parts = line.split('|')
            for part in parts:
                match = re.search(md_button_pattern, part.strip())
                if match:
                    btn_text = match.group(1).strip()
                    btn_type = match.group(2)
                    btn_value = match.group(3).strip()
                    
                    if btn_type == 'url':
                        row.append(InlineKeyboardButton(text=btn_text, url=btn_value))
                    elif btn_type == 'callback':
                        row.append(InlineKeyboardButton(text=btn_text, callback_data=btn_value))
        
        # Then check for simple format (Text | URL)
        elif '|' in line:
            # Check for multiple pairs in one line
            # Format: Btn1 | Link1 | Btn2 | Link2
            # We split by | and process in pairs
            parts = [p.strip() for p in line.split('|')]
            # If we have even number of parts (text, url, text, url...)
            # Or if it's Btn | Link | something else, we take pairs
            for i in range(0, len(parts) - 1, 2):
                btn_text = parts[i]
                btn_url = parts[i+1]
                
                # Check if it looks like a URL
                if re.match(r'https?://[^\s]+', btn_url):
                    row.append(InlineKeyboardButton(text=btn_text, url=btn_url))
        
        if row:
            buttons.append(row)
        else:
            clean_text.append(line)
    
    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
    return '\n'.join(clean_text).strip(), reply_markup


async def auto_clean():
    while not await asyncio.sleep(10):
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(
                        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
                    ):
                        if user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except:
            continue


asyncio.create_task(auto_clean())
