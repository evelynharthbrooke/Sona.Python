import arrow
import discord
from discord import ApplicationContext, SlashCommandGroup
from discord import Member
from discord.ext import commands

from client import Client


class Spotify(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    spotify = SlashCommandGroup("spotify", "rovides access to retrieving data from the Spotify API.")

    @spotify.command()
    async def album(self, context: ApplicationContext, id: str = None, name: str = None, artist: str = None, year: int = None, market: str = None) -> None:
        """Retrieves a specific album from Spotify. Defaults to the current Spotify activity if available.

        Parameters
        ----------
        id: The album id. Optional if name or activity is provided, required if not.
        name: The album name. Optional if id or activity is provided, required if not.
        artist: The artist who recorded the album. Optional.
        year: The year the album was recorded. Optional.
        market: The region to be searched, as a two-character country code. Optional.
        """
        if id is None and name is None:
            if context.guild is not None and len(context.author.activities) >= 1:
                activity = context.author.activity
                if isinstance(activity, discord.Spotify):
                    track = self.client.spotify.track(activity.track_id, market)
                    album = self.client.spotify.album(track["album"]["id"], market)
                    tracks = self.client.spotify.album_tracks(track["album"]["id"], market=market)["items"]
                else:
                    return await context.respond("No current Spotify activity. Please provide an album name or id.")
            else:
                return await context.respond("Please provide either an album name or album id.")
        elif id is not None and name is None:
            album = self.client.spotify.album(id, market)
            tracks = self.client.spotify.album_tracks(id, market=market)["items"]
        elif name is not None and id is None:
            query = f"album: {name}{f' artist: {artist}' if artist else ''}{f' year: {year}' if year else ''}"
            results = self.client.spotify.search(query, 1, 0, "album", market)
            if len(results["albums"]["items"]) > 0:
                album = self.client.spotify.album(results["albums"]["items"][0]["id"], market)
                tracks = self.client.spotify.album_tracks(album["id"], market=market)["items"]
            else:
                return await context.respond("No albums were found matching this criteria.")
        else:
            return await context.respond("You cannot provide both an album name and album id.")

        title = album["name"]
        url = album["external_urls"]["spotify"]
        length = 0
        artists = list()
        tracklist = list()

        for artist in album["artists"]:
            a_name = artist["name"]
            a_url = artist["external_urls"]["spotify"]
            artists.append(f"[{a_name}]({a_url})")

        for track in tracks:
            length += track["duration_ms"] / 1000

            if context.guild is not None and len(context.author.activities) >= 1:
                activity = context.author.activity
                if isinstance(activity, discord.Spotify):
                    a_title = activity.title
                    t_name = f"**{track['name']}**" if a_title in track["name"] else track["name"]
            else:
                t_name = track["name"]

            t_pos = track["track_number"]
            t_url = track["external_urls"]["spotify"]
            t_explicit = track["explicit"]
            t_time = track["duration_ms"] / 1000
            t_length = arrow.get(t_time).format("h [hr] m [min] s [sec]" if t_time > 3600 else "m [min] s [sec]")

            tracklist.append(f"**{t_pos}**. [{t_name}]({t_url}){'  🅴' if t_explicit else ''} - {t_length}")

        embed = discord.Embed(title=title, url=url, description="\n".join(tracklist), color=0x1DB954)
        embed.set_thumbnail(url=album["images"][0]["url"])
        embed.add_field(name="Artist(s)", value=", ".join(artists), inline=True)
        embed.add_field(name="Length", value=arrow.get(length).format("h [hr] m [min] s [sec]" if length > 3600 else "m [min] s [sec]"), inline=True)
        embed.add_field(name="Released", value=arrow.get(album["release_date"]).format("MMM D, YYYY"), inline=True)
        embed.add_field(name="Tracks", value=album["total_tracks"], inline=True)
        embed.add_field(name="Type", value=album["album_type"].title() if len(tracks) <= 1 or len(tracks) > 7 else "Extended Play (EP)", inline=True)

        try:
            # due to a quirk in the spotify api, the available_markets array is omitted from the
            # response if the market name is provided, as i guess for some reason spotify doesn't
            # see a point to providing the array if you're searching for an album in a specific
            # market.
            if len(album["available_markets"]) > 0:
                embed.add_field(name="Markets", value=len(album["available_markets"]), inline=True)
            else:
                embed.add_field(name="Markets", value="None (Delisted)", inline=True)
        except KeyError:
            # insert empty field if we get a key error to avoid running into a discord bug
            # regarding embeds where if there are only two fields in a row, the discord client
            # will push the 2nd field to the right.
            embed.insert_field_at(5, name=b"\u200B", value=b"\u200B", inline=True)

        embed.set_footer(text="Powered by the Spotify Web API.")

        await context.respond(embed=embed)

    @spotify.command()
    async def track(self, context: ApplicationContext, id: str = None, name: str = None, market: str = None) -> None:
        """Retrieves information about Spotify tracks.

        Parameters
        ----------
        id: The track id. Not required if name or activity is provided, required if not.
        name: The track name. Not required if id or activity is provided, required if not.
        market: The region to be searched, as a two-character country code. Optional.
        """
        if id is None and name is None:
            if context.guild is not None and len(context.author.activities) >= 1:
                activity = context.author.activity
                if isinstance(activity, discord.Spotify):
                    track = self.client.spotify.track(activity.track_id, market)
                else:
                    return await context.respond("No current Spotify activity found.")
            else:
                return await context.respond("You must provide either a track name or id.")
        elif id is not None and name is None:
            track = self.client.spotify.track(id, market=market)
        elif id is None and name is not None:
            result = self.client.spotify.search(name, 1, 0, "track", market)
            items = result["tracks"]["items"]
            if len(items) > 0:
                track = self.client.spotify.track(items[0]["id"], market)
            else:
                return await context.respond("No tracks were found matching this criteria.")
        else:
            return await context.respond("You cannot provide both a track id and name.")

        album = track["album"]["name"]
        album_url = track["album"]["external_urls"]["spotify"]
        length = track["duration_ms"] / 1000
        artists = list()

        for artist in track["artists"]:
            artist_name = artist["name"]
            artist_url = artist["external_urls"]["spotify"]
            artists.append(f"[{artist_name}]({artist_url})")

        embed = discord.Embed(title=f"{track['name']} {'🅴' if track['explicit'] else ''}", url=track["external_urls"]["spotify"], color=0x1DB954)
        embed.set_thumbnail(url=track["album"]["images"][0]["url"])
        embed.add_field(name="Artists", value=", ".join(artists), inline=True)
        embed.add_field(name="Album", value=f"[{album}]({album_url})", inline=True)
        embed.add_field(name="Released", value=arrow.get(track["album"]["release_date"]).format("MMM D, YYYY"), inline=True)
        embed.add_field(name="Length", value=arrow.get(length).format("h [hr] m [min] s [sec]" if length > 3600 else "m [min] s [sec]"), inline=True)

        try:
            if len(track["available_markets"]) > 0:
                embed.add_field(name="Markets", value=len(track["available_markets"]), inline=True)
            else:
                embed.add_field(name="Markets", value="None (Delisted)", inline=True)
        except KeyError:
            embed.insert_field_at(4, name="\u200B", value="\u200B", inline=True)

        embed.add_field(name="\u200B", value="\u200B", inline=True)
        embed.set_footer(text="Powered by the Spotify Web API.")

        await context.respond(embed=embed)

    @spotify.command()
    async def status(self, context: ApplicationContext, member: Member = None) -> None:
        """Retrieves a given user's Spotify status. Defaults to your own."""
        if context.guild is None:
            # due to the way discord activities work, they cannot be accessed from direct
            # messages for some reason, so disallow the command from being used in guilds
            # to avoid it breaking.
            return await context.respond("This command cannot be used from DMs.")

        member = context.author if member is None else member
        if member.bot:
            return await context.respond("Bots can't listen to music, silly.")

        name = member.name.title()

        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                title = activity.title
                artist = activity.artist
                album = activity.album
                message = f"**{name}** is currently listening to **{title}** by **{artist}** on **{album}**."
                if member is context.author:
                    message = f"You are currently listening to **{title}** by **{artist}** on **{album}**."
                return await context.respond(message)

        if member is context.author:
            return await context.respond("You aren't currently istening to anything.")

        await context.respond(f"**{name}** isn't currently listening to anything.")


def setup(client: Client):
    client.add_cog(Spotify(client))
