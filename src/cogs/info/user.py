from disnake import Spotify
from disnake.ext.commands import Cog, Context, command

from client import Client


class User(Cog):
    @command()
    async def id(self, context: Context):
        """Retrieves the message author's user ID."""

        name = context.author.name.title()
        id = context.author.id

        await context.channel.send(f"Hello **{name}**, your user ID is `{id}`.")

    @command()
    async def status(self, context: Context):
        """Retrieves a user's current Spotify status."""
        user = context.author.name
        activity = context.author.activity

        if isinstance(activity, Spotify):
            title = activity.title
            artist = activity.artist
            album = activity.album
            return await context.channel.send(f"**{user}** is listening to **{title}** by **{artist}** on **{album}**.")

        await context.channel.send(f"**{user}** is not listening to anything.")


def setup(bot: Client):
    bot.add_cog(User(bot))
