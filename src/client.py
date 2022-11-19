import logging
import platform
import sys

import arrow
import disnake
import psutil
from disnake.ext import commands
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

with open("./config.toml", mode="rb") as c:
    config = tomllib.load(c)

sp_client_id = config["network"]["spotify"]["client_id"]
sp_client_secret = config["network"]["spotify"]["client_secret"]

logger = logging.getLogger()


class Client(commands.AutoShardedInteractionBot):
    def __init__(self):
        super().__init__(intents=disnake.Intents.all())
        self.uptime = arrow.now()
        self.process = psutil.Process()
        self.spotify = Spotify(auth_manager=SpotifyClientCredentials(client_id=sp_client_id, client_secret=sp_client_secret))

    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    async def on_ready(self):
        logger.info("-" * 30)
        logger.info("Disnake Information:" )
        logger.info("-" * 30)
        logger.info("Version:            %s", disnake.__version__)
        logger.info("Python:             %s", platform.python_version())
        logger.info("-" * 30)
        logger.info("Discord Bot Information:")
        logger.info("-" * 30)
        logger.info("Bot name:           %s", self.user)
        logger.info("Bot id:             %d", self.user.id)
        logger.info("Bot owner:          %s", self.owner)
        logger.info("Bot created:        %s", self.user.created_at)
        logger.info("Total shards:       %d", self.shard_count)
        logger.info("Total servers:      %d", len(self.guilds))
        logger.info("Total channels:     %d", len(set(self.get_all_channels())))
        logger.info("Total users:        %d", len(set(self.get_all_members())))
        logger.info("Total commands:     %d", len(self.slash_commands))
        logger.info("Total cogs:         %d", len(self.cogs))

    def run(self, *args, **kwargs):
        self.load_extension("cogs.info.bot")
        self.load_extension("cogs.info.user")
        self.load_extension("cogs.misc.network")
        self.load_extension("cogs.network.services.github")
        self.load_extension("cogs.network.services.mastodon")
        self.load_extension("cogs.network.services.spotify")
        return super().run(*args, **kwargs)
