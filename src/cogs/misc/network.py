import re

import requests
from disnake.ext.commands import Cog, Context, command

from client import Client


class Network(Cog):
    """Commands that interface with web services & APIs."""

    @command("kernel", aliases=["linux"])
    async def kernel(self, context: Context):
        """Retrieves information about various Linux kernel versions."""

        request = requests.get("https://www.kernel.org/finger_banner").text
        regex = re.sub(r"The latest(\s*)", "**", request)
        regex_b = re.sub(r"version of the Linux kernel is:(\s*)", "**- ", regex).split("\n")
        versions = "\n".join(version for version in regex_b[:-1])
        message = f"**__Available Linux Kernel Versions:__**\n\n{versions}"

        await context.send(message)


def setup(bot: Client):
    bot.add_cog(Network(bot))
