from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from client import Client


class Utilities(commands.Cog):
    """Miscellaneous commands that don't belong in other cogs."""

    @commands.slash_command()
    async def source(self, interaction: ApplicationCommandInteraction) -> None:
        """Retrieves a link to the bot's repository on either GitHub or GitLab."""

        await interaction.response.send_message(f"You can view Sona's git repository here: <https://github.com/evelynmarie/Sona>")


def setup(client: Client):
    client.add_cog(Utilities(client))
