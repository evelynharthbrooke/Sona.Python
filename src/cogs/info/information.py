import platform

import arrow
import discord
import psutil
from discord.ext import commands

from sona import SonaClient
from utilities.util import retrieve_cpu_name


class Information(commands.Cog):
    def __init__(self, bot: SonaClient):
        self.bot = bot

    @commands.command("about", aliases=["info"])
    async def about(self, context: commands.Context):
        """
        Retrieves information about the bot.
        """

        avatar_url = self.bot.user.avatar_url
        name = self.bot.user.name
        users = len(self.bot.users)
        guilds = len(self.bot.guilds)
        uptime = self.bot.uptime.humanize()

        # Python version information
        python = platform.python_version()
        revision = platform.python_revision()

        dcord = discord.__version__
        commands = len(self.bot.commands)
        cogs = len(self.bot.cogs)

        embed = discord.Embed(color=discord.Color.blurple())
        embed.set_author(icon_url=avatar_url, name=name)

        embed.add_field(name="__**Basic Info:**__", value=f'**Started:** {uptime}\n'
                                                          f'**Users:** {users}\n'
                                                          f'**Guilds:** {guilds}')
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="__**Statistics:**__", value=f'**Discord.py:** {dcord}\n'
                                                          f'**Commands:** {commands}\n'
                                                          f'**Cogs loaded:** {cogs}')
        embed.add_field(name="__**Python:**__", value=f'**Version:** {python}\n'
                                                      f'**Revision:** {revision}\n')
        embed.set_footer(text=f'{name} user ID: {self.bot.user.id}')

        return await context.send(embed=embed)

    @commands.command("system", aliases=["sys"])
    async def system(self, ctx: commands.Context):
        """
        Gets information about the host system.
        """
        avatar_url = self.bot.user.avatar_url
        name = self.bot.user.name

        # CPU details
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_usage = f'{psutil.cpu_percent(interval=0.1)}%'
        cpu_frequency = f'{psutil.cpu_freq(False).current / 1000}'

        # Generic system statistics and information
        system_type = platform.machine()
        system_uptime = arrow.get(psutil.boot_time()).humanize()

        # Memory information
        mem_total = round(psutil.virtual_memory().total / 1048576)
        mem_used = round(psutil.virtual_memory().used / 1048576)
        mem_free = round(psutil.virtual_memory().free / 1048576)

        # Information related to the bot's process
        proc_threads = self.bot.process.num_threads()
        proc_cpu_usage = round(self.bot.process.cpu_percent())
        proc_mem_used = round(
            self.bot.process.memory_full_info().rss / 1048576)
        proc_id = self.bot.process.pid

        embed = discord.Embed(color=discord.Color.blurple())
        embed.set_author(icon_url=avatar_url, name=f'{name} System Statistics')
        embed.description = f'Information about {name}\'s host system.'
        embed.add_field(name="__**CPU:**__", value=f'**Cores:** {cpu_cores}\n'
                                                   f'**Threads:** {cpu_threads}\n'
                                                   f'**Usage:** {cpu_usage}\n'
                                                   f'**Frequency:** {cpu_frequency} GHz')
        embed.add_field(name="__**System:**__", value=f'**Started:** {system_uptime}\n'
                                                      f'**System type:** {system_type}')
        embed.add_field(name="__**Memory:**__", value=f'**Total:** {mem_total} MiB\n'
                                                      f'**Used:** {mem_used} MiB\n'
                                                      f'**Free:** {mem_free} MiB', inline=False)
        embed.add_field(name="__**Process:**__", value=f'**Memory usage:** {proc_mem_used} MiB\n'
                                                       f'**Threads:** {proc_threads}\n'
                                                       f'**CPU usage:**: {proc_cpu_usage}%')
        embed.set_footer(text=f'{name} process identifier: {proc_id}')

        return await ctx.send(embed=embed)


def setup(bot: SonaClient):
    bot.add_cog(Information(bot))
