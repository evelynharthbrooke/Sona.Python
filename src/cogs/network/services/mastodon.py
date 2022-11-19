import requests
import json

import disnake
from disnake import ApplicationCommandInteraction as Interaction
from disnake.ext import commands
import markdownify

from client import Client


class Mastodon(commands.Cog):
    @commands.slash_command()
    async def mastodon(self, inter: Interaction) -> None:
        del inter  # delete inter as we aren't using it
        pass

    @mastodon.sub_command()
    async def user(self, inter: Interaction, instance: str, user: str) -> None:
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
            return await inter.send("No users were found that match this criteria.")

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

        embed = disnake.Embed(title=member, url=url, description=markdownify.markdownify(note))
        embed.set_thumbnail(url=avatar)

        for field in result["fields"]:
            name = field["name"]
            value = markdownify.markdownify(field["value"])
            if "http://" in value or "https://" in value:
                value = markdownify.markdownify(f"[{name}]({field['value']})")
            embed.add_field(name, value)
            pass

        embed.add_field("Posts", statuses)
        embed.add_field("Following", following)
        embed.add_field("Followers", followers)

        if len(embed.fields) < 6:
            embed.add_field("\u200B", "\u200B")

        await inter.send(embed=embed)

    @mastodon.sub_command_group()
    async def instance(self, inter: Interaction) -> None:
        del inter  # delete inter as we aren't using it
        pass

    @instance.sub_command()
    async def info(self, inter: Interaction, instance: str) -> None:
        """Retrieves information about a given Mastodon instance.

        Parameters
        ----------
        instance: the Mastodon instance to get information about.
        """
        request = requests.get(f"https://{instance}/api/v1/instance")
        response = json.loads(request.text)

        url = response["uri"]
        title = response["title"]
        description = markdownify.markdownify(response["description"])
        version = response["version"]
        thumbnail = response["thumbnail"]
        registrations = response["registrations"]
        approval_required = response["approval_required"]
        posts = response["stats"]["status_count"]
        users = response["stats"]["user_count"]
        federated_instances = response["stats"]["domain_count"]

        rules = list()
        rule_id = 0
        for rule in response["rules"]:
            rule_id += 1
            rule_text = rule['text'].strip('\n')
            rules.append(f"{rule_id}. {rule_text}\n")

        embed = disnake.Embed(title=title, description=f"{description}\n\n**Server Rules**: \n{''.join(rules)}", url=f"https://{url}")
        embed.set_thumbnail(url=thumbnail)
        embed.add_field("Posts on Instance", posts)
        embed.add_field("Users on Instance", users)
        embed.add_field("Federated With", f"{federated_instances} instances")
        embed.add_field("Registrations Open", "Yes" if registrations else "No")
        embed.add_field("Approval Required", "Yes" if approval_required else "No")
        embed.add_field("Mastodon Version", version)
        embed.set_footer(text="Powered by the Mastodon API.")

        return await inter.send(embed=embed)


def setup(client: Client):
    client.add_cog(Mastodon(client))
