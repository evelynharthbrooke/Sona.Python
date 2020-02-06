import logging

import discord
import toml

from sona import SonaClient

from discord import ActivityType
from discord.ext import commands
from discord.ext.commands import AutoShardedBot, when_mentioned_or

config = toml.load('./config.toml')
token = config['general']['api']['token']
token_two = config['general']['api']['token_two']

bot = SonaClient()

bot.run(token_two)
