import asyncio
import importlib

from pyrogram import idle
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
    
    # Start everything in parallel for faster startup
    await asyncio.gather(
        app.start(),
        userbot.start(),
        JARVIS.start(),
        return_exceptions=True
    )
    
    await sudo()
    
    # Load banned users asynchronously (non-blocking)
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"Failed to load banned users: {e}")
    
    # Load all modules quickly
    for all_module in ALL_MODULES:
        importlib.import_module("ANNIEMUSIC.plugins" + all_module)
    LOGGER("ANNIEMUSIC.plugins").info("ʙʀᴏᴋᴇɴ x ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ...")
    
    # Skip test stream call for faster startup
    await JARVIS.decorators()
    
    # Start auto maintenance scheduler in background
    from ANNIEMUSIC.plugins.misc.auto_maintenance import start_maintenance_scheduler
    asyncio.create_task(start_maintenance_scheduler())
    
    LOGGER("MUSICBROKN").info("Annie Music Robot Started Successfully...")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("MUSICBROKN").info("sᴛᴏᴘᴘɪɴɢ ʙʀᴏᴋᴇɴ x ᴍᴜsɪᴄ ʙᴏᴛ ...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
