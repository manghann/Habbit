# Original concept by Timothy Manabat (@tkmanabat)
# https://github.com/tkmanabat/RoboMark
# Rewritten and optimized by github.com/manghann

from discord.ext import commands
import discord
import youtube_dl
import ffmpeg
import asyncio

youtube_dl.utils.bug_reports_message=lambda:''
queueSong=[]

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command(name='play', help='This command plays some music from youtube')
    async def play(self,ctx,url):
        if not ctx.message.author.voice:
            await ctx.send('Connect to Voice Channel, please! (•ㅅ•)')
            return
        else:
            channel= ctx.message.author.voice.channel

        if not is_connected(ctx):
            await channel.connect()

        global queueSong
        queueSong.append(url)

        server=ctx.message.guild
        voiceChannel=server.voice_client

        async with ctx.typing():
            player=await YTDLSource.from_url(queueSong[0], loop=self.client.loop,stream=True)
            voiceChannel.play(player, after=lambda e: print('Player error: %s' %e) if e else None)
            del(queueSong[0])

        await ctx.send(f'**Now playing:** `{player.title}` 🎶')

    @commands.command(name='queue')
    async def queue(self, ctx, url):
        global queueSong
        queueSong.append(url)
        await ctx.send(f"Music added: `{url}` ")

    @commands.command(name='remove')
    async def remove(self,ctx, number):
        global queueSong
        try:
            del(queueSong[int(number)])
            await ctx.send(f'On queue: `{queueSong}`')
        except :
            await ctx.send('No more music to play ₍ᐢ ̥ ̞ ̥ᐢ₎?')

    @commands.command(name='view', help='show the queue')
    async def view(self,ctx):
        await ctx.send(f"Music Queue: `{queueSong}`")


    @commands.command(name='join')
    async def join(self,ctx):
        if not ctx.message.author.voice:
            await ctx.send('Connect to Voice Channel, please! (•ㅅ•)')
            return
        else:
            channel= ctx.message.author.voice.channel

        await channel.connect()


    @commands.command(name='stop', help='This command stops the music currently playing.')
    async def stop(self,ctx):
        queueSong.clear()
        voiceClient= ctx.message.guild.voice_client
        #await voiceClient.disconnect()


def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def setup(client):
    client.add_cog(Music(client))