from disnake import ApplicationCommandInteraction, Member, Spotify
from disnake.channel import PartialMessageable
from disnake.ext import commands

from client import Client


class User(commands.Cog):
    @commands.slash_command()
    async def id(interaction: ApplicationCommandInteraction):
        """Retrieves the message author's user ID."""

        name = interaction.author.name.title()
        id = interaction.author.id

        await interaction.response.send_message(f"Hello **{name}**, your user ID is `{id}`.")

    @commands.slash_command()
    async def status(interaction: ApplicationCommandInteraction, member: Member = None):
        """Retrieves a given user's Spotify status."""

        if isinstance(interaction.channel, PartialMessageable):
            return await interaction.response.send_message("This command cannot be used in DMs.")
        elif member is None:
            member = interaction.author
        elif member.bot:
            return await interaction.response.send_message("Bots can't listen to music, silly.")

        name = member.name.title()
        activity = member.activity

        if isinstance(activity, Spotify):
            title = activity.title
            artist = activity.artist
            album = activity.album
            message = f"**{name}** is listening to **{title}** by **{artist}** on **{album}**."
            return await interaction.response.send_message(message)

        await interaction.response.send_message(f"**{name}** is not listening to anything.")


def setup(bot: Client):
    bot.add_cog(User(bot))
