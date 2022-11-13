from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from client import Client


class Github(commands.Cog):
    """A set of commands for interacting with the GitHub API."""

    @commands.slash_command()
    async def github(self, inter: ApplicationCommandInteraction) -> None:
        del inter

    @github.sub_command()
    async def user(self, inter: ApplicationCommandInteraction) -> None:
        """Retrieves information about a GitHub user."""
        await inter.send("This command is a work in progress.")

    @github.sub_command()
    async def repository(self, inter: ApplicationCommandInteraction) -> None:
        """Retrieves information about a GitHub repository."""
        await inter.send("This command is a work in progress.")


def setup(client: Client):
    client.add_cog(Github(client))
