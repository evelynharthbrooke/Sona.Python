from disnake import Message
from disnake.ext.commands import Cog, Context, command

from client import Client


class User(Cog):
    @command("id")
    async def id(self, context: Context):
        """Retrieves the message author's user ID."""

        name = context.author.name.title()
        id = context.author.id

        await context.channel.send(f"Hello **{name}**, your user ID is `{id}`.")


def setup(bot: Client):
    bot.add_cog(User(bot))
