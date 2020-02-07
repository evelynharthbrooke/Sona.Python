import logging
import pathlib
import sys
import time
from platform import python_version

import arrow
import discord
import psutil
import toml
from discord.ext import commands

config = toml.load('./config.toml')
owners = config['general']['bot']['owners']
prefixes = config['general']['bot']['prefixes']
debug = config['general']['bot']['debug']

log = logging.getLogger()


class SonaClient(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(*prefixes),
                         case_insensitive=True,
                         description="A bot built for the Discord chat platform with Disccord.py.",
                         help_command=commands.DefaultHelpCommand())
        self.owners = owners,
        self.uptime = arrow.now()
        # add the bot's current process as a available property.
        self.process = psutil.Process()
        self.database = None
        self.prefixes = {}

    handler = logging.StreamHandler(sys.stdout)
    log.addHandler(handler)

    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    async def is_owner(self, user):
        return user.id in self.owners or await super().is_owner(user)

    async def on_ready(self):
        if self.owner_id is None:
            app = await self.application_info()
            self.owner_id = app.owner.id

        log.info("-" * 23)
        log.info("Discord.py Information:")
        log.info("-" * 23)
        log.info("Version:            %s", discord.__version__)
        log.info("Python:             %s", python_version())
        log.info("-" * 24)
        log.info("Discord Bot Information:")
        log.info("-" * 24)
        log.info("User name:          %s", self.user)
        log.info("User ID:            %d", self.user.id)
        log.info("Created at:         %s", self.user.created_at)
        log.info("Total users:        %d", len(set(self.get_all_members())))
        log.info("Total channels:     %d", len(set(self.get_all_channels())))
        log.info("Total servers:      %d", len(self.guilds))
        log.info("Total commands:     %s", len(self.commands))
        log.info("Total cogs:         %s", len(self.cogs))
        log.info("Debug mode:         %s", str(debug))

    def run(self, *args, **kwargs):
        self.load_extension('jishaku')
        self.load_extension('cogs.info.information')
        return super().run(*args, **kwargs)
