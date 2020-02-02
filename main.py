import logging

import discord
import toml
from discord import Activity, ActivityType
from discord.ext import commands
from discord.ext.commands import AutoShardedBot, when_mentioned_or

config = toml.load('config.toml')
token = config['general']['api']['token']
prefixes = config['general']['bot']['prefixes']

bot = AutoShardedBot(command_prefix=when_mentioned_or(*prefixes))


@bot.event
async def on_ready():
    activity = Activity(type=ActivityType.playing, name="test")
    print('Logged in as {0}#{1}'.format(bot.user.name, bot.user.discriminator))
    await bot.change_presence(activity=activity)

bot.run(token, reconnect=True)
