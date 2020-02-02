import logging

import discord
import toml
from discord.ext import commands
from discord.ext.commands import AutoShardedBot, when_mentioned_or

config = toml.load('config.toml')
token = config['general']['api']['token']
prefixes = config['general']['bot']['prefixes']

bot = AutoShardedBot(command_prefix=when_mentioned_or(*prefixes))


@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: {0}'.format(bot.user.name))
    print('ID: {0}'.format(bot.user.id))

bot.run(token, reconnect=True)
