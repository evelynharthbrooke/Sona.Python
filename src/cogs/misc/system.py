import arrow
import psutil
from disnake import ApplicationCommandInteraction, Color, Embed
from disnake.ext import commands

from client import Client


class System(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.slash_command()
    async def system(self, inter: ApplicationCommandInteraction):
        """Gets information about the host system."""

        name = self.client.user.name
        avatar = self.client.user.avatar.url

        cores = psutil.cpu_count(logical=False)
        threads = psutil.cpu_count(logical=True)
        load = f"{psutil.cpu_percent(interval=0.1)}%"
        freq = f"{psutil.cpu_freq(False).current / 1000}"

        uptime = arrow.get(psutil.boot_time()).humanize()

        mem_total = round(psutil.virtual_memory().total / 1048576)
        mem_used = round(psutil.virtual_memory().used / 1048576)
        mem_free = round(psutil.virtual_memory().free / 1048576)

        proc_threads = self.client.process.num_threads()
        proc_load = round(self.client.process.cpu_percent())
        proc_mem = round(self.client.process.memory_full_info().rss / 1048576)
        proc_id = self.client.process.pid

        embed = Embed(color=Color.blurple())
        embed.description = f"Information about {name}'s host system."
        embed.set_author(name=f"{name} System Statistics", icon_url=avatar)
        embed.add_field("__**CPU:**__", value=f"**Cores:** {cores}\n**Threads:** {threads}\n**Load:** {load}\n**Frequency:** {freq} GHz")
        embed.add_field("\u200B", "\u200B")
        embed.add_field("__**System:**__", value=f"**Started:** {uptime}")
        embed.add_field("__**Memory:**__", value=f"**Total:** {mem_total} MiB\n**Used:** {mem_used} MiB\n**Free:** {mem_free} MiB")
        embed.add_field("\u200B", "\u200B")
        embed.add_field("__**Process:**__", value=f"**Memory:** {proc_mem} MiB\n**Threads:** {proc_threads}\n**CPU:** {proc_load}%")
        embed.set_footer(text=f"{name} process identifier: {proc_id}")

        await inter.response.send_message(embed=embed)
        pass


def setup(client: Client):
    client.add_cog(System(client))
