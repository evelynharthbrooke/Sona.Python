from enum import Enum

from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from client import Client

class Service(int, Enum):
    """The service to fetch the git repository from."""
    GitHub = 0
    GitLab = 1

class Utilities(commands.Cog):
    def __init__(self, bot: Client) -> None:
        self.bot = bot

    @commands.slash_command()
    async def source(self, interaction: ApplicationCommandInteraction, service: Service = Service.GitHub) -> None:
        """Retrieves a link to the bot's GitHub repository."""

        if service == Service.GitHub:
            repository = "https://github.com/evelynmarie/Sona"
        elif service == Service.GitLab:
            repository = "https://gitlab.com/evelynmarie/Sona"

        await interaction.response.send_message(f"You can view Sona's git repository here: <{repository}>")

def setup(bot: Client):
    bot.add_cog(Utilities(bot))
