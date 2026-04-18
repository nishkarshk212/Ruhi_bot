import asyncio

# Setup event loop for Python 3.12+ / 3.14+
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import importlib
from pyrogram import filters, idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ANNIEMUSIC import LOGGER, app, userbot
from ANNIEMUSIC.core.call import JARVIS
from ANNIEMUSIC.misc import sudo
from ANNIEMUSIC.plugins import ALL_MODULES
from ANNIEMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("ᴀssɪsᴛᴀɴᴛ sᴇssɪᴏɴ ɴᴏᴛ ғɪʟʟᴇᴅ, ᴘʟᴇᴀsᴇ ғɪʟʟ ᴀ ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴ...")
        exit()
    
    # Start bot
    await app.start()

    # Start userbot
    await userbot.start()
    LOGGER("MUSICBROKN").info("Userbot client started")

    # Start PyTgCalls
    await JARVIS.start()
    LOGGER("MUSICBROKN").info("PyTgCalls client started")

    # Load sudo users
    await sudo()

    # Load banned users
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"Failed to load banned users: {e}")

    # Load all modules
    for all_module in ALL_MODULES:
        importlib.import_module("ANNIEMUSIC.plugins" + all_module)
    LOGGER("ANNIEMUSIC.plugins").info("ʙʀᴏᴋᴇɴ x ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ...")

    # Register decorators
    await JARVIS.decorators()

    # Start auto maintenance scheduler in background
    from ANNIEMUSIC.plugins.misc.auto_maintenance import start_maintenance_scheduler
    asyncio.create_task(start_maintenance_scheduler())

    LOGGER("MUSICBROKN").info("Annie Music Robot Started Successfully...")
    LOGGER("MUSICBROKN").info("Bot is now listening for messages...")

    # This will keep the bot running and processing updates
    await idle()
    
    LOGGER("MUSICBROKN").info("sᴛᴏᴘᴘɪɴɢ ʙʀᴏᴋᴇɴ x ᴍᴜsɪᴄ ʙᴏᴛ ...")
    await app.stop()
    await userbot.stop()


if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init())
    except KeyboardInterrupt:
        LOGGER("MUSICBROKN").info("Bot stopped by user")
    except Exception as e:
        LOGGER("MUSICBROKN").error(f"Bot crashed: {e}")
