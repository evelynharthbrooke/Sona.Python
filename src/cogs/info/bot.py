import platform

from disnake import ApplicationCommandInteraction, Color, Embed
from disnake import __version__ as disnake_version
from disnake.ext import commands

from client import Client
from constants import hash, version


class Bot(commands.Cog):
    """Retrieves information about the bot."""

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.slash_command()
    async def bot(self, _: ApplicationCommandInteraction) -> None:
        pass

    @bot.sub_command()
    async def about(self, interaction: ApplicationCommandInteraction) -> None:
        """Retrieves information about the bot."""

        avatar_url = self.client.user.avatar.url
        name = self.client.user.name
        users = len(self.client.users)
        guilds = len(self.client.guilds)
        uptime = self.client.uptime.humanize()
        python = platform.python_version()
        commands = len(self.client.slash_commands)
        cogs = len(self.client.cogs)

        embed = Embed(color=Color.blurple())
        embed.set_author(name=name, icon_url=avatar_url)
        embed.add_field("__**Basic Info:**__", f"**Started:** {uptime}\n**Version:** {version} (rev. {hash})\n**Users:** {users}\n**Guilds:** {guilds}")
        embed.add_field("\u200B", "\u200B")
        embed.add_field("__**Statistics:**__", f"**Disnake:** {disnake_version}\n**Python:** {python}\n**Commands:** {commands}\n**Cogs:** {cogs}")
        embed.set_footer(text=f"{name} user ID: {self.client.user.id}")

        await interaction.response.send_message(embed=embed)

    @bot.sub_command()
    async def source(self, interaction: ApplicationCommandInteraction) -> None:
        """Retrieves a link to the bot's repository."""
        await interaction.response.send_message(f"You can view Sona's git repository here: <https://github.com/evelynmarie/Sona>")


def setup(client: Client):
    client.add_cog(Bot(client))
