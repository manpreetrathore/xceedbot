from discord import Embed, FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get

from youtube_dl import YoutubeDL
from asyncio import run_coroutine_threadsafe
import requests

class Music(commands.Cog, name='Music'):
    """
    Can be used by anyone and allows you to listen to music or videos.
    """
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.message = {}

    @staticmethod
    def parse_duration(duration):
        result = []
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)
        return f'{h:d}:{m:02d}:{s:02d}'

    @staticmethod
    def search(author, arg):
        print(1)
        await ctx.send("Getting things ready.")
        print(2)
        with YoutubeDL(Music.YDL_OPTIONS) as ydl:
            try: requests.get(arg)
            except: info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else: info = ydl.extract_info(arg, download=False)

        embed = (Embed(title='🎵 Now playing:', description=f"[{info['title']}]({info['webpage_url']})", color=0x3498db)
                .add_field(name='Duration', value=Music.parse_duration(info['duration']))
                .add_field(name='Asked by', value=author)
                .add_field(name='Uploader', value=f"[{info['uploader']}]({info['channel_url']})")
                .add_field(name="Queue", value=f"No queued videos")
                .set_thumbnail(url=info['thumbnail']))

        return {'embed': embed, 'source': info['formats'][0]['url'], 'title': info['title']}
    async def ensure_voice(self,ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
    async def edit_message(self, ctx):
        embed = self.song_queue[ctx.guild][0]['embed']
        content = "\n".join([f"({self.song_queue[ctx.guild].index(i)}) {i['title']}" for i in self.song_queue[ctx.guild][1:]]) if len(self.song_queue[ctx.guild]) > 1 else "No queued videos"
        embed.set_field_at(index=3, name="Queue:", value=content, inline=False)
        await self.message[ctx.guild].edit(embed=embed)

    def play_next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if len(self.song_queue[ctx.guild]) > 1:
            del self.song_queue[ctx.guild][0]
            run_coroutine_threadsafe(self.edit_message(ctx), self.bot.loop)
            voice.play(FFmpegPCMAudio(self.song_queue[ctx.guild][0]['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
            voice.is_playing()
        else:
            run_coroutine_threadsafe(voice.disconnect(), self.bot.loop)
            run_coroutine_threadsafe(self.message[ctx.guild].delete(), self.bot.loop)

    @commands.command(aliases=['p'], brief='!play [url/words]', description='Listen to a video from an url or from a youtube search')
    async def play(self, ctx, *, video: str):

        try:
            channel = ctx.author.voice.channel
            if not channel:
                await ctx.send("Go in a voice channel to listen to music.")
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            song = Music.search(ctx.author.mention, video)

            if voice and voice.is_connected():
                await voice.move_to(channel)

            else:
                voice = await channel.connect()
                #voice.play(discord.FFmpegPCMAudio(executable="C:/path/ffmpeg.exe", source="mp3.mp3"))
            await ctx.message.delete()
            if not voice.is_playing():

                self.song_queue[ctx.guild] = [song]
                self.message[ctx.guild] = await ctx.send(embed=song['embed'])
                # voice.play(FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                voice.is_playing()
            else:

                self.song_queue[ctx.guild].append(song)
                await self.edit_message(ctx)
        except TypeError:
            await ctx.send("Go in a voice channel to listen to music.")

    @commands.command(brief='!pause', description='Pause the current video', aliases=['resume'])
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_connected():
            await ctx.message.delete()
            if voice.is_playing():
                await ctx.send('⏸️ Music paused', delete_after=5.0)
                voice.pause()
            else:
                await ctx.send('⏯️ Music resumed', delete_after=5.0)
                voice.resume()

    @commands.command(brief='!skip', description='Skip the current video')
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.message.delete()
            await ctx.send('⏭️ Musique skipped', delete_after=5.0)
            voice.stop()

    @commands.command(brief='!remove [index]', description='Remove a song from the queue')
    async def remove(self, ctx, *, num: int):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            del self.song_queue[ctx.guild][num]
            await ctx.message.delete()
            await self.edit_message(ctx)

    # @commands.command()
    # async def volume(self, ctx, volume: int):
    #     """Changes the player's volume"""
    #
    #     if ctx.voice_client is None:
    #         return await ctx.send("Not connected to a voice channel.")
    #
    #     ctx.voice_client.source.volume = volume / 100
    #     await ctx.send("Changed volume to {}%".format(volume))
     # @commands.command(name='volume', aliases=['volume'])
     # async def vol(self, ctx, *, vol: float):
     #    """Change the player volume.
     #    Parameters
     #    ------------
     #    volume: float or int [Required]
     #        The volume to set the player to in percentage. This must be between 1 and 100.
     #    """
     #    vc = ctx.voice_client
     #
     #    if not vc or not vc.is_connected():
     #        return await ctx.send('I am not currently connected to voice!', delete_after=20)
     #
     #    if not 0 < vol < 101:
     #        return await ctx.send('Please enter a value between 1 and 100.')
     #
     #    player = self.get_player(ctx)
     #
     #    if vc.source:
     #        vc.source.volume = vol / 100
     #
     #    player.volume = vol / 100
     #    await ctx.send(f'**`{ctx.author}`**: Set the volume to **{vol}%**')

def setup(bot):
    bot.add_cog(Music(bot))
