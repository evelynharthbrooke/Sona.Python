import re

import requests
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from client import Client


class Network(commands.Cog):
    """Commands that interface with web services & APIs."""

    @commands.slash_command()
    async def kernel(self, inter: ApplicationCommandInteraction):
        """Retrieves the latest available Linux kernel versions."""

        request = requests.get("https://www.kernel.org/finger_banner").text
        regex = re.sub(r"The latest(\s*)", "**", request)
        regex_b = re.sub(r"version of the Linux kernel is:(\s*)", "**- ", regex).split("\n")
        versions = "\n".join(version for version in regex_b[:-1])
        message = f"**__Available Linux Kernel Versions:__**\n\n{versions}"

        await inter.send(message)
        pass


def setup(client: Client):
    client.add_cog(Network(client))
    pass
