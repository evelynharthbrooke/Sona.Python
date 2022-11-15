import arrow
from disnake import ApplicationCommandInteraction, Member
from disnake.ext import commands

from client import Client


class User(commands.Cog):
    """A set of commands for interacting with users."""

    @commands.slash_command()
    async def user(self, inter: ApplicationCommandInteraction) -> None:
        """Retrieve information about users."""
        del inter

    @user.sub_command()
    async def id(self, inter: ApplicationCommandInteraction, member: Member = None) -> None:
        """Retrieves a user's account ID. Defaults to your own account."""

        user = inter.author if member is None else member
        name = user.name.title()
        id = user.id

        if user is inter.author:
            return await inter.send(f"Hello **{name}**, your user ID is _{id}_.")

        await inter.send(f"The user ID for **{name}** is _{id}_.")

    @user.sub_command()
    async def age(self, inter: ApplicationCommandInteraction, member: Member = None) -> None:
        """Retrieves a user's account age. Defaults to your own account."""

        user = inter.author if member is None else member
        name = user.name
        joined = arrow.get(user.created_at).format("MMMM D, YYYY")
        joined_humanized = arrow.get(user.created_at).humanize(granularity=["year", "week", "day"])

        if user is inter.author:
            return await inter.send(f"You joined Discord on {joined}, or _{joined_humanized}_.")

        await inter.send(f"**{name}** joined Discord on {joined}, or _{joined_humanized}_.")


def setup(client: Client):
    client.add_cog(User(client))
