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
    
    # Start everything in parallel for faster startup (1-2 seconds)
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
    except:
        pass
    
    # Load all modules quickly
    for all_module in ALL_MODULES:
        importlib.import_module("ANNIEMUSIC.plugins" + all_module)
    LOGGER("ANNIEMUSIC.plugins").info("ʙʀᴏᴋᴇɴ x ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ...")
    
    # Skip test stream call for faster startup
    await JARVIS.decorators()
    
    # Start auto maintenance scheduler in background
    from ANNIEMUSIC.plugins.misc.auto_maintenance import start_maintenance_scheduler
    asyncio.create_task(start_maintenance_scheduler())
    
    LOGGER("MUSICBROKN").info(
        "\x41\x6e\x6e\x69\x65\x20\x4d\x75\x73\x69\x63\x20\x52\x6f\x62\x6f\x74\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\x2e\x2e"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("MUSICBROKN").info("sᴛᴏᴘᴘɪɴɢ ʙʀᴏᴋᴇɴ x ᴍᴜsɪᴄ ʙᴏᴛ ...")
