import arrow
import discord
from discord import ApplicationContext, Member
from discord.ext import commands

from client import Client


class User(commands.Cog):
    """A set of commands for interacting with users."""

    user = discord.SlashCommandGroup("user", "Interact with users / members.")

    @user.command()
    async def id(self, context: ApplicationContext, member: Member = None) -> None:
        """Retrieves a user's account ID. Defaults to your own account."""

        user = context.author if member is None else member
        name = user.name.title()
        id = user.id

        if user is context.author:
            return await context.respond(f"Hello **{name}**, your user ID is _{id}_.")

        await context.respond(f"The user ID for **{name}** is _{id}_.")

    @user.command()
    async def age(self, context: ApplicationContext, member: Member = None) -> None:
        """Retrieves a user's account age. Defaults to your own account."""

        user = context.author if member is None else member
        name = user.name
        joined = arrow.get(user.created_at).format("MMMM D, YYYY")
        joined_humanized = arrow.get(user.created_at).humanize(granularity=["year", "week", "day"])

        if user is context.author:
            return await context.respond(f"You joined Discord on {joined}, or _{joined_humanized}_.")

        await context.respond(f"**{name}** joined Discord on {joined}, or _{joined_humanized}_.")


def setup(client: Client):
    client.add_cog(User(client))
