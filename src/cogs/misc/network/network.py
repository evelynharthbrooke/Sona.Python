import re

import discord
import requests
from discord.ext import commands

from sona import SonaClient


class Network(commands.Cog):
    """
    Various network-based commands.
    """

    def __init__(self, bot: SonaClient):
        self.bot = bot

    @commands.command("kernel", aliases=["linux"])
    async def kernel(self, context: commands.Context):
        """
        Retrieves information about various Linux kernel versions.
        """
        kernel_request = requests.get(
            "https://www.kernel.org/finger_banner").text
        regex_b = re.sub(r"The latest(\s*)", '**', kernel_request)
        regex_b = re.sub(r"version of the Linux kernel is:(\s*)", '**- ',
                         regex_b)

        lines = regex_b.split("\n")
        versions = "\n".join(line for line in lines[:-1])

        message = f'**__Available Linux Kernel Versions:__**\n\n{versions}'
        return await context.send(message)


def setup(bot: SonaClient):
    bot.add_cog(Network(bot))
