import platform

import arrow
import psutil
from disnake import ApplicationCommandInteraction, Color, Embed
from disnake import __version__ as disnake_version
from disnake.ext import commands

from client import Client
from constants import hash, version


class Information(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot

    @commands.slash_command()
    async def about(self, interaction: ApplicationCommandInteraction):
        """Retrieves information about the bot."""

        avatar_url = self.bot.user.avatar.url
        name = self.bot.user.name
        users = len(self.bot.users)
        guilds = len(self.bot.guilds)
        uptime = self.bot.uptime.humanize()

        python = platform.python_version()

        commands = len(self.bot.slash_commands)
        cogs = len(self.bot.cogs)

        embed = Embed(color=Color.blurple())
        embed.set_author(name=name, icon_url=avatar_url)
        embed.add_field("__**Basic Info:**__", f"**Started:** {uptime}\n**Version:** {version} (rev. {hash})\n**Users:** {users}\n**Guilds:** {guilds}")
        embed.add_field("\u200B", "\u200B")
        embed.add_field("__**Statistics:**__", f"**Disnake:** {disnake_version}\n**Python:** {python}\n**Commands:** {commands}\n**Cogs:** {cogs}")
        embed.set_footer(text=f"{name} user ID: {self.bot.user.id}")

        await interaction.response.send_message(embed=embed)

    @commands.slash_command()
    async def system(self, interaction: ApplicationCommandInteraction):
        """Gets information about the host system."""
        avatar_url = self.bot.user.avatar.url
        name = self.bot.user.name

        cores = psutil.cpu_count(logical=False)
        threads = psutil.cpu_count(logical=True)
        load = f"{psutil.cpu_percent(interval=0.1)}%"
        freq = f"{psutil.cpu_freq(False).current / 1000}"

        arch = platform.machine()
        uptime = arrow.get(psutil.boot_time()).humanize()

        mem_total = round(psutil.virtual_memory().total / 1048576)
        mem_used = round(psutil.virtual_memory().used / 1048576)
        mem_free = round(psutil.virtual_memory().free / 1048576)

        proc_threads = self.bot.process.num_threads()
        proc_load = round(self.bot.process.cpu_percent())
        proc_mem = round(self.bot.process.memory_full_info().rss / 1048576)
        proc_id = self.bot.process.pid

        embed = Embed(color=Color.blurple())
        embed.description = f"Information about {name}'s host system."
        embed.set_author(name=f"{name} System Statistics", icon_url=avatar_url)
        embed.add_field("__**CPU:**__", value=f"**Cores:** {cores}\n**Threads:** {threads}\n**Load:** {load}\n**Frequency:** {freq} GHz")
        embed.add_field("\u200B", "\u200B")
        embed.add_field("__**System:**__", value=f"**Started:** {uptime}\n**Type:** {arch}")
        embed.add_field("__**Memory:**__", value=f"**Total:** {mem_total} MiB\n**Used:** {mem_used} MiB\n**Free:** {mem_free} MiB")
        embed.add_field("\u200B", "\u200B")
        embed.add_field("__**Process:**__", value=f"**Memory:** {proc_mem} MiB\n**Threads:** {proc_threads}\n**CPU:** {proc_load}%")
        embed.set_footer(text=f"{name} process identifier: {proc_id}")

        await interaction.response.send_message(embed=embed)


def setup(bot: Client):
    bot.add_cog(Information(bot))
