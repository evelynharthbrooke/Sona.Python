import platform
import arrow
import discord
import psutil
from discord import ApplicationContext, SlashCommandGroup, Color, Embed, __version__ as discord_version
from discord.ext import commands

from client import Client
from constants import hash, version


class Bot(commands.Cog):
    """Retrieves information about the bot."""

    def __init__(self, client: Client) -> None:
        self.client = client

    bot = discord.SlashCommandGroup("bot", "Retrieve information about the bot.")

    @bot.command()
    async def about(self, context: ApplicationContext) -> None:
        """Retrieves information about the bot."""

        name = self.client.user.name
        avatar = self.client.user.avatar.url
        users = len(self.client.users)
        guilds = len(self.client.guilds)
        uptime = self.client.uptime.humanize()
        python = platform.python_version()

        embed = Embed(color=Color.blurple())
        embed.set_author(name=name, icon_url=avatar)
        embed.add_field(name="Started", value=uptime, inline=True)
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="Version", value=f"{version} (rev. `{hash}`)", inline=True)
        embed.add_field(name="Users", value=users, inline=True)
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="Guilds", value=guilds, inline=True)
        embed.set_footer(text=f"{name} user ID: {self.client.user.id}")

        await context.respond(embed=embed)

    @bot.command()
    async def system(self, context: ApplicationContext):
        """Gets information about the bot's host system."""

        name = self.client.user.name
        avatar = self.client.user.avatar.url

        cores = psutil.cpu_count(logical=False)
        threads = psutil.cpu_count(logical=True)
        load = f"{psutil.cpu_percent(interval=0.1)}%"
        freq = f"{psutil.cpu_freq(False).current / 1000} GHz"

        uptime = arrow.get(psutil.boot_time()).humanize()

        mem_total = f"{round(psutil.virtual_memory().total / 1048576)} MiB"
        mem_used = f"{round(psutil.virtual_memory().used / 1048576)} MiB"
        mem_free = f"{round(psutil.virtual_memory().free / 1048576)} MiB"

        proc_threads = self.client.process.num_threads()
        proc_load = f"{round(self.client.process.cpu_percent())}%"
        proc_mem = f"{round(self.client.process.memory_full_info().rss / 1048576)} MiB"
        proc_id = self.client.process.pid

        embed = Embed(color=Color.blurple())
        embed.description = f"Information about {name}'s host system."
        embed.set_author(name=f"{name} System Statistics", icon_url=avatar)
        embed.add_field(name="__**CPU:**__", value=f"**Cores:** {cores}\n**Threads:** {threads}\n**Load:** {load}\n**Frequency:** {freq}")
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="__**System:**__", value=f"**Started:** {uptime}")
        embed.add_field(name="__**Memory:**__", value=f"**Total:** {mem_total}\n**Used:** {mem_used}\n**Free:** {mem_free}")
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="__**Process:**__", value=f"**Memory:** {proc_mem}\n**Threads:** {proc_threads}\n**CPU:** {proc_load}")
        embed.set_footer(text=f"{name} process identifier: {proc_id}")

        await context.respond(embed=embed)

    @bot.command()
    async def source(self, context: ApplicationContext) -> None:
        """Retrieves a link to the bot's repository."""
        await context.respond(f"You can view Sona's git repository here: <https://github.com/evelynmarie/Sona>")


def setup(client: Client):
    client.add_cog(Bot(client))
