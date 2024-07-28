import re
import requests
import discord
from discord import ApplicationContext
from discord.ext import commands

from client import Client


class Network(commands.Cog):
    """Commands that interface with web services & APIs."""

    @discord.slash_command()
    async def kernel(self, context: ApplicationContext):
        """Retrieves the latest available Linux kernel versions."""

        request = requests.get("https://www.kernel.org/finger_banner").text
        regex = re.sub(r"The latest(\s*)", "**", request)
        regex_b = re.sub(r"version of the Linux kernel is:(\s*)", "**- ", regex).split("\n")
        versions = "\n".join(version for version in regex_b[:-1])
        message = f"**__Available Linux Kernel Versions:__**\n\n{versions}"

        await context.respond(message)


def setup(client: Client):
    client.add_cog(Network(client))
