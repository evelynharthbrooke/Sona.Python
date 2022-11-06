from disnake import ApplicationCommandInteraction, Spotify
from disnake.ext import commands

from client import Client


class User(commands.Cog):
    @commands.slash_command()
    async def id(interaction: ApplicationCommandInteraction):
        """Retrieves the message author's user ID."""

        name = interaction.author.name.title()
        id = interaction.author.id

        await interaction.channel.send(f"Hello **{name}**, your user ID is `{id}`.")

    @commands.slash_command()
    async def status(interaction: ApplicationCommandInteraction):
        """Retrieves a user's current Spotify status."""
        user = interaction.author.name.title()
        activity = interaction.author.activity

        if isinstance(activity, Spotify):
            title = activity.title
            artist = activity.artist
            album = activity.album
            message = f"**{user}** is listening to **{title}** by **{artist}** on **{album}**."
            return await interaction.response.send_message(message)

        await interaction.response.send_message(f"**{user}** is not listening to anything.")


def setup(bot: Client):
    bot.add_cog(User(bot))
