import arrow
import discord
from discord.ext import commands

from sona import SonaClient
from utilities.util import retrieve_cpu_name


class Info(commands.Cog, name='Information'):
    def __init__(self, bot: SonaClient):
        self.bot = bot

    @commands.command("about", aliases=["info"])
    async def about(self, context: commands.Context):
        """
        Retrieves information about Sona.
        """

        avatar_url = self.bot.user.avatar_url
        name = self.bot.user.name
        users = len(self.bot.users)
        guilds = len(self.bot.guilds)
        uptime = self.bot.uptime.humanize()

        dcord = discord.__version__
        commands = len(self.bot.commands)
        cogs = len(self.bot.cogs)

        embed = discord.Embed(color=discord.Color.blurple())
        embed.set_author(icon_url=avatar_url, name=name)

        embed.add_field(name="__**Basic Info:**__", value=f'**Started:** {uptime}\n'
                                                          f'**Users:** {users}\n'
                                                          f'**Guilds:** {guilds}')
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="__**Statistics:**__", value=f'**Discord.py:** {dcord}\n'
                                                          f'**Commands:** {commands}\n'
                                                          f'**Cogs loaded:** {cogs}')
        
        embed.set_footer(text=f'Sona user ID: {self.bot.user.id}')

        return await context.send(embed=embed)

    @commands.command("system", aliases=["sys"])
    async def system(self, ctx: commands.Context):
        """
        Gets information about the host system.
        """
        get_cpu = await retrieve_cpu_name(ctx)
        cpu = ''.join(c for c in get_cpu if c.lower() not in '('')')
        return await ctx.send(f'CPU Name: {cpu}')


def setup(bot: SonaClient):
    bot.add_cog(Info(bot))
