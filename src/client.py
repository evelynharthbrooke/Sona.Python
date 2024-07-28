import logging
import platform
import sys

import arrow
import constants
import discord
import psutil
from discord.ext import commands
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

with open("./config.toml", mode="rb") as c:
    config = tomllib.load(c)

logger = logging.getLogger()
hb_timeout = config["general"]["heartbeat_timeout"]
sp_client_id = config["network"]["spotify"]["client_id"]
sp_client_secret = config["network"]["spotify"]["client_secret"]


class Client(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), heartbeat_timeout=hb_timeout)
        self.uptime = arrow.now()
        self.process = psutil.Process()
        self.spotify = Spotify(auth_manager=SpotifyClientCredentials(client_id=sp_client_id, client_secret=sp_client_secret))

    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    async def on_ready(self):
        logger.info("-" * 30)
        logger.info("Version Information:")
        logger.info("-" * 30)
        logger.info("Python version:     %s", platform.python_version())
        logger.info("Pycord version:     %s", discord.__version__)
        logger.info("Bot version:        %s", constants.version)
        logger.info("-" * 30)
        logger.info("Discord Bot Information:")
        logger.info("-" * 30)
        logger.info("Bot name:           %s", self.user)
        logger.info("Bot id:             %d", self.user.id)
        logger.info("Bot created:        %s", self.user.created_at)
        logger.info("Total shards:       %d", self.shard_count)
        logger.info("Total servers:      %d", len(self.guilds))
        logger.info("Total channels:     %d", len(set(self.get_all_channels())))
        logger.info("Total users:        %d", len(set(self.get_all_members())))

    def run(self, *args, **kwargs):
        self.load_extension("cogs.info.bot")
        self.load_extension("cogs.info.user")
        self.load_extension("cogs.misc.network")
        self.load_extension("cogs.network.services.github")
        self.load_extension("cogs.network.services.mastodon")
        self.load_extension("cogs.network.services.spotify")
        return super().run(*args, **kwargs)
