# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic


import pyrogram

from billu import config, logger


class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
            name="billu",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=pyrogram.enums.ParseMode.HTML,
            max_concurrent_transmissions=7,
            link_preview_options=pyrogram.types.LinkPreviewOptions(is_disabled=True),
        )
        self.owner = config.OWNER_ID
        self.logger = config.LOGGER_ID
        self.bl_users = pyrogram.filters.user()
        self.sudoers = pyrogram.filters.user(self.owner)

    async def boot(self):
        """
        Starts the bot and performs initial setup.

        Raises:
            SystemExit: If the bot fails to access the log group or is not an administrator in the logger group.
        """
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        # Set bot commands
        await self.set_bot_commands([
            pyrogram.types.BotCommand("start", "Start the bot"),
            pyrogram.types.BotCommand("help", "Show help menu"),
            pyrogram.types.BotCommand("play", "Play a song"),
            pyrogram.types.BotCommand("vplay", "Play a video"),
            pyrogram.types.BotCommand("playforce", "Force play a song"),
            pyrogram.types.BotCommand("vplayforce", "Force play a video"),
            pyrogram.types.BotCommand("pause", "Pause current song"),
            pyrogram.types.BotCommand("resume", "Resume current song"),
            pyrogram.types.BotCommand("skip", "Skip current song"),
            pyrogram.types.BotCommand("stop", "Stop playback"),
            pyrogram.types.BotCommand("loop", "Loop current song"),
            pyrogram.types.BotCommand("queue", "Show queue"),
            pyrogram.types.BotCommand("playing", "Show currently playing"),
            pyrogram.types.BotCommand("seek", "Seek forward"),
            pyrogram.types.BotCommand("seekback", "Seek backward"),
            pyrogram.types.BotCommand("auth", "Authorize a user"),
            pyrogram.types.BotCommand("unauth", "Unauthorize a user"),
            pyrogram.types.BotCommand("authlist", "List authorized users"),
            pyrogram.types.BotCommand("ping", "Check ping"),
            pyrogram.types.BotCommand("alive", "Check if bot is alive"),
            pyrogram.types.BotCommand("stats", "Show bot stats"),
            pyrogram.types.BotCommand("lang", "Change language"),
            pyrogram.types.BotCommand("language", "Change language"),
            pyrogram.types.BotCommand("settings", "Bot settings"),
            pyrogram.types.BotCommand("playmode", "Bot settings"),
            pyrogram.types.BotCommand("restart", "Restart the bot"),
            pyrogram.types.BotCommand("logs", "Get logs"),
        ])

        try:
            await self.send_message(self.logger, "Bot Started")
            get = await self.get_chat_member(self.logger, self.id)
        except Exception as ex:
            raise SystemExit(f"Bot has failed to access the log group: {self.logger}\nReason: {ex}")

        if get.status != pyrogram.enums.ChatMemberStatus.ADMINISTRATOR:
            raise SystemExit("Please promote the bot as an admin in logger group.")
        logger.info(f"Bot started as @{self.username}")

    async def exit(self):
        """
        Asynchronously stops the bot.
        """
        await super().stop()
        logger.info("Bot stopped.")
