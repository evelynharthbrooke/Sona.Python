import logging
import platform
import sys

import arrow
import disnake
import psutil
from disnake.ext import commands

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

with open("./config.toml", mode="rb") as c:
    config = tomllib.load(c)

owners = config["general"]["bot"]["owners"]
prefixes = config["general"]["bot"]["prefixes"]

logger = logging.getLogger()


class Client(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(commands.when_mentioned_or(*prefixes), commands.DefaultHelpCommand(), intents=disnake.Intents.all())
        self.owners = owners
        self.uptime = arrow.now()
        self.process = psutil.Process()
        self.database = None
        self.prefixes = {}

    logger.addHandler(logging.StreamHandler(sys.stdout))

    async def is_owner(self, user):
        return user.id in self.owners or await super().is_owner(user)

    async def on_ready(self):
        if self.owner_id is None:
            app = await self.application_info()
            self.owner_id = app.owner.id

        logger.info("-" * 23)
        logger.info("Disnake Information:")
        logger.info("-" * 23)
        logger.info("Version:            %s", disnake.__version__)
        logger.info("Python:             %s", platform.python_version())
        logger.info("-" * 24)
        logger.info("Discord Bot Information:")
        logger.info("-" * 24)
        logger.info("User name:          %s", self.user)
        logger.info("User ID:            %d", self.user.id)
        logger.info("Created at:         %s", self.user.created_at)
        logger.info("Total users:        %d", len(set(self.get_all_members())))
        logger.info("Total channels:     %d", len(set(self.get_all_channels())))
        logger.info("Total servers:      %d", len(self.guilds))
        logger.info("Total commands:     %s", len(self.commands))
        logger.info("Total cogs:         %s", len(self.cogs))

    def run(self, *args, **kwargs):
        self.load_extension("cogs.info.information")
        self.load_extension("cogs.info.user")
        self.load_extension("cogs.misc.network")
        return super().run(*args, **kwargs)
