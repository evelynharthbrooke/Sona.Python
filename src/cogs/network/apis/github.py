from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from client import Client


class Github(commands.Cog):
    """A set of commands for interacting with the GitHub API."""

    @commands.slash_command()
    async def github(self, inter: ApplicationCommandInteraction) -> None:
        pass

    @github.sub_command()
    async def user(self, inter: ApplicationCommandInteraction) -> None:
        """Retrieves information about a GitHub user."""
        await inter.response.send_message("This command is a work in progress.")
        pass

    @github.sub_command()
    async def repository(self, inter: ApplicationCommandInteraction) -> None:
        """Retrieves information about a GitHub repository."""
        await inter.response.send_message("This command is a work in progress.")
        pass


def setup(client: Client):
    client.add_cog(Github(client))
    pass
