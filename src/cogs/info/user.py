from disnake import ApplicationCommandInteraction, Member, Spotify
from disnake.ext import commands

from client import Client


class User(commands.Cog):
    @commands.slash_command()
    async def id(interaction: ApplicationCommandInteraction, member: Member = None) -> None:
        """Retrieves the user ID for a given user."""

        if member is None:
            # Default to the message sender if no member is provided.
            member = interaction.author

        name = member.name.title()
        id = member.id

        if member is interaction.author:
            return await interaction.response.send_message(f"Hello **{name}**, your user ID is _{id}_.")

        await interaction.response.send_message(f"The user ID for **{name}** is _{id}_.")


def setup(client: Client):
    client.add_cog(User(client))
