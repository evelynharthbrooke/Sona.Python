import arrow
import disnake
from disnake import ApplicationCommandInteraction as Interaction
from disnake import Member
from disnake.ext import commands

from client import Client


class Spotify(commands.Cog):
    """A set of commands for interacting with Spotify."""

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.slash_command()
    async def spotify(self, inter: Interaction) -> None:
        """Provides access to retrieving data from the Spotify API."""
        del inter  # delete inter as we aren't using it
        pass

    @spotify.sub_command()
    async def album(self, inter: Interaction, id: str = None, name: str = None, artist: str = None, year: int = None, market: str = None) -> None:
        """
        Retrieves a specific album from Spotify. Defaults to the current Spotify activity if available.

        Parameters
        ----------
        id: The album id. Optional if name or activity is provided, required if not.
        name: The album name. Optional if id or activity is provided, required if not.
        artist: The artist who recorded the album. Optional.
        year: The year the album was recorded. Optional.
        market: The region to be searched, as a two-character country code. Optional.
        """

        if id is not None and name is None:
            album = self.client.spotify.album(id, market)
            tracks = self.client.spotify.album_tracks(id, market=market)["items"]
        elif name is not None and id is None:
            if artist is not None and year is None:
                query = f"album: {name} artist: {artist}"
            elif artist is None and year is not None:
                query = f"album: {name} year: {year}"
            elif artist is not None and year is not None:
                query = f"album: {name} artist: {artist} year: {year}"
            else:
                query = f"album: {name}"

            results = self.client.spotify.search(query, 1, 0, "album", market)

            if len(results["albums"]["items"]) > 0:
                album = self.client.spotify.album(results["albums"]["items"][0]["id"], market)
                tracks = self.client.spotify.album_tracks(album["id"], market=market)["items"]
            else:
                return await inter.send("No albums were found matching this criteria.")
        elif name is not None and id is not None:
            return await inter.send("You cannot provide both an album name and album id.")
        else:
            if len(inter.author.activities) >= 1:
                activity = inter.author.activity
                if isinstance(activity, disnake.Spotify):
                    track = self.client.spotify.track(activity.track_id, market)
                    album = self.client.spotify.album(track["album"]["id"], market)
                    tracks = self.client.spotify.album_tracks(track["album"]["id"], market=market)["items"]
                else:
                    return await inter.send("No current Spotify activity. Please provide an album name or id.")
            else:
                return await inter.send("Please provide either an album name or album id.")

        name = album["name"]
        id = album["id"]
        duration = 0
        released = arrow.get(album["release_date"]).format("MMM D, YYYY")
        type = album["album_type"].title() if len(tracks) <= 1 or len(tracks) > 7 else "Extended Play (EP)"
        artists = list()
        tracklist = list()

        for artist in album["artists"]:
            artist_name = artist["name"]
            artist_url = artist["external_urls"]["spotify"]
            artists.append(f"[{artist_name}]({artist_url})")

        for track in tracks:
            title = track["name"]
            position = track["track_number"]
            url = track["external_urls"]["spotify"]
            dur_ms = track["duration_ms"] / 1000
            length = arrow.get(dur_ms).format("h [hr] m [min] s [sec]" if dur_ms > 3600 else "m [min] s [sec]")

            if track["explicit"]:
                tracklist.append(f"**{position}**. [{title}]({url}) **E** - {length}")
            else:
                tracklist.append(f"**{position}**. [{title}]({url}) - {length}")

            duration += track["duration_ms"] / 1000

        embed = disnake.Embed(color=0x1DB954)
        embed.title = name
        embed.url = f"https://open.spotify.com/album/{id}"
        embed.description = "\n".join(tracklist)
        embed.set_thumbnail(album["images"][0]["url"])  # use largest image available
        embed.add_field("Type", type, inline=True)
        embed.add_field("Released", released, inline=True)
        embed.add_field("Artists", ", ".join(artists), inline=True)
        embed.add_field("Tracks", album["total_tracks"], inline=True)

        if duration > 3600:
            embed.add_field("Length", arrow.get(duration).format("h [hr] m [min] s [sec]"), inline=True)
        else:
            embed.add_field("Length", arrow.get(duration).format("m [min] s [sec]"), inline=True)

        try:
            # due to a quirk in the spotify api, the available_markets array is omitted from the
            # response if the market name is provided, as i guess for some reason spotify doesn't
            # see a point to providing the array if you're searching for an album in a specific
            # market.
            if len(album["available_markets"]) > 0:
                embed.add_field("Markets", len(album["available_markets"]), inline=True)
            else:
                embed.add_field("Markets", "None (Delisted)", inline=True)
        except KeyError:
            # insert empty field if we get a key error to avoid running into a discord bug
            # regarding embeds where if there are only two fields in a row, the discord client
            # will push the 2nd field to the right.
            embed.insert_field_at(5, "\u200B", "\u200B", inline=True)

        embed.set_footer(text="Powered by the Spotify Web API.")

        await inter.send(embed=embed)

    @spotify.sub_command()
    async def track(self, inter: Interaction, id: str = None, name: str = None, market: str = None) -> None:
        """Retrieves information about Spotify tracks.

        Parameters
        ----------
        id: The track id. Not required if name or activity is provided, required if not.
        name: The track name. Not required if id or activity is provided, required if not.
        market: The region to be searched, as a two-character country code. Optional.
        """

        if id is not None and name is None:
            track = self.client.spotify.track(id, market=market)
        elif id is None and name is not None:
            result = self.client.spotify.search(name, 1, 0, "track", market)
            items = result["tracks"]["items"]
            if len(items) > 0:
                track = self.client.spotify.track(items[0]["id"], market)
            else:
                return await inter.send("No tracks were found matching this criteria.")
        elif id is not None and name is not None:
            return await inter.send("You cannot provide both a track id and name.")
        else:
            if len(inter.author.activities) > 0:
                activity = inter.author.activity
                if isinstance(activity, disnake.Spotify):
                    track = self.client.spotify.track(activity.track_id, market)
                else:
                    return await inter.send("No current Spotify activity found.")
            else:
                return await inter.send("You must provide either a track name or id.")

        album = track["album"]["name"]
        album_url = track["album"]["external_urls"]["spotify"]
        duration = track["duration_ms"] / 1000
        artists = list()

        for artist in track["artists"]:
            artist_name = artist["name"]
            artist_url = artist["external_urls"]["spotify"]
            artists.append(f"[{artist_name}]({artist_url})")

        embed = disnake.Embed(color=0x1DB954)
        embed.title = track["name"]
        embed.url = track["external_urls"]["spotify"]
        embed.set_thumbnail(track["album"]["images"][0]["url"])
        embed.add_field("Album", f"[{album}]({album_url})", inline=True)
        embed.add_field("Released", arrow.get(track["album"]["release_date"]).format("MMM D, YYYY"), inline=True)

        if duration > 3600:
            embed.add_field("Length", arrow.get(duration).format("h [hr] m [min] s [sec]"), inline=True)
        else:
            embed.add_field("Length", arrow.get(duration).format("m [min] s [sec]"), inline=True)

        embed.add_field("Artists", ", ".join(artists), inline=True)
        embed.add_field("Explicit", "Yes" if track["explicit"] else "No", inline=True)

        try:
            embed.add_field("Markets", len(track["album"]["available_markets"]), inline=True)
        except KeyError:
            embed.insert_field_at(5, "\u200B", "\u200B", inline=True)

        embed.set_footer(text="Powered by the Spotify Web API.")

        await inter.send(embed=embed)

    @spotify.sub_command()
    async def status(self, inter: Interaction, member: Member = None) -> None:
        """Retrieves a given user's Spotify status. Defaults to your own."""

        if inter.guild_id is None:
            # due to the way discord activities work, they cannot be accessed from direct
            # messages for some reason, so disallow the command from being used in guilds
            # to avoid it breaking.
            return await inter.send("This command cannot be used from DMs.")

        if member is None:
            member = inter.author
        elif member.bot:
            return await inter.send("Bots can't listen to music, silly.")

        name = member.name.title()
        activity = member.activity

        if isinstance(activity, disnake.Spotify):
            title = activity.title
            artist = activity.artist
            album = activity.album

            if member is inter.author:
                message = f"You are currently listening to **{title}** by **{artist}** on **{album}**."
            else:
                message = f"**{name}** is currently listening to **{title}** by **{artist}** on **{album}**."

            return await inter.send(message)

        if member is inter.author:
            return await inter.send("You aren't currently istening to anything.")

        await inter.send(f"**{name}** isn't currently listening to anything.")


def setup(client: Client):
    client.add_cog(Spotify(client))
