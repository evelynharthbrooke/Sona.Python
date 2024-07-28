import discord
from discord import ApplicationContext
from discord.ext import commands

from client import Client


class Github(commands.Cog):
    """A set of commands for interacting with the GitHub API."""

    github = discord.SlashCommandGroup("github", "Interact with GitHub.")

    @github.command()
    async def user(self, context: ApplicationContext) -> None:
        """Retrieves information about a GitHub user."""
        await context.respond("This command is a work in progress.")

    @github.command()
    async def repository(self, context: ApplicationContext) -> None:
        """Retrieves information about a GitHub repository."""
        await context.respond("This command is a work in progress.")


def setup(client: Client):
    client.add_cog(Github(client))
