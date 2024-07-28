import discord
import json
import requests
from discord import ApplicationContext, Embed
from discord.ext import commands
from markdownify import markdownify

from client import Client


class Mastodon(commands.Cog):
    mastodon = discord.SlashCommandGroup("mastodon", "Commands for interacting with the Mastodon social network.")
    instance = mastodon.create_subgroup("instance", "Commands related to Mastodon instances")

    @mastodon.command()
    async def user(self, context: ApplicationContext, instance: str, user: str) -> None:
        """View information about a user on the Mastodon federated social network.

        Parameters
        ----------
        instance: the hostname of the instance to connect to.
        user: the user on the instance to look up.
        """

        endpoint = requests.get(f"https://{instance}/api/v2/search?q={user}&limit=50")
        response = json.loads(endpoint.text)
        result = response["accounts"]

        if len(result) < 1:
            return await context.respond("No users were found that match this criteria.")

        for account in result:
            if account["acct"] == user:
                result = account

        member = result["display_name"]
        avatar = result["avatar"]
        url = result["url"]
        note = result["note"]
        statuses = result["statuses_count"]
        following = result["following_count"]
        followers = result["followers_count"]

        embed = Embed(title=member, url=url, description=markdownify(note))
        embed.set_thumbnail(url=avatar)

        for field in result["fields"]:
            name = field["name"]
            value = markdownify(field["value"])
            if "http://" in value or "https://" in value:
                value = markdownify(f"[{name}]({field['value']})")
            embed.add_field(name=name, value=value)
            pass

        embed.add_field(name="Posts", value=statuses)
        embed.add_field(name="Following", value=following)
        embed.add_field(name="Followers", value=followers)

        if len(embed.fields) < 6:
            embed.add_field(name="\u200B", value="\u200B")

        await context.respond(embed=embed)

    @instance.command()
    async def info(self, context: ApplicationContext, instance: str) -> None:
        """Retrieves information about a given Mastodon instance.

        Parameters
        ----------
        instance: the Mastodon instance to get information about.
        """

        request = requests.get(f"https://{instance}/api/v1/instance")
        response = json.loads(request.text)

        url = response["uri"]
        title = response["title"]
        description = markdownify(response["description"])
        version = response["version"]
        thumbnail = response["thumbnail"]
        registrations = response["registrations"]
        approval_required = response["approval_required"]
        posts = response["stats"]["status_count"]
        users = response["stats"]["user_count"]
        federated_instances = response["stats"]["domain_count"]

        rules = []
        rule_id = 0
        for rule in response["rules"]:
            rule_id += 1
            rule_text = rule["text"].strip("\n")
            rules.append(f"{rule_id}. {rule_text}\n")

        embed_desc = description + ("\n\n**__Server Rules__**:\n" + "".join(rules) if len(rules) > 0 else "")

        embed = Embed(title=title, description=embed_desc, url=f"https://{url}")
        embed.set_thumbnail(thumbnail)
        embed.add_field(name="Posts on Instance", value=posts)
        embed.add_field(name="Users on Instance", value=users)
        embed.add_field(name="Federated With", value=f"{federated_instances} instances")
        embed.add_field(name="Registrations Open", value="Yes" if registrations else "No")
        embed.add_field(name="Approval Required", value="Yes" if approval_required else "No")
        embed.add_field(name="Mastodon Version", value=version)
        embed.set_footer(text="Powered by the Mastodon API.")

        return await context.respond(embed=embed)


def setup(client: Client):
    client.add_cog(Mastodon(client))
