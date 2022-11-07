from enum import Enum

from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from client import Client


class Service(int, Enum):
    GitHub = 0
    GitLab = 1


class Utilities(commands.Cog):
    """Miscellaneous commands that don't belong in other cogs."""

    @commands.slash_command()
    async def source(interaction: ApplicationCommandInteraction, service: Service = Service.GitHub) -> None:
        """Retrieves a link to the bot's repository on either GitHub or GitLab."""

        if service == Service.GitHub:
            repository = "https://github.com/evelynmarie/Sona"
        elif service == Service.GitLab:
            repository = "https://gitlab.com/evelynmarie/Sona"

        await interaction.response.send_message(f"You can view Sona's git repository here: <{repository}>")


def setup(bot: Client):
    bot.add_cog(Utilities(bot))
