"""Cog for a discord bot, uses a discord.VoiceClient to play sounds"""

import asyncio
from tempfile import NamedTemporaryFile

import discord
from discord.ext import commands
from utils import Utils


if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus-0.x86.dll')


def disconnect(voice, loop):
    """Disconnect from VoiceChannel"""

    print("nothing prints and bot doesn't disconnect")
    coro = voice.disconnect
    fut = asyncio.run_coroutine_threadsafe(coro, loop)
    fut.result()


class Sound:
    """Different commands for playing sounds"""

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)


    @commands.command()
    async def play(self, ctx, *, args=None):
        """Play a `mp3` file that was sent over discord as an attachment"""

        if not ctx.author.voice:
            return await ctx.send("You're not connected to a voice channel.")

        with NamedTemporaryFile(delete=False) as fp:
            await ctx.message.attachments[0].save(fp)
        to_play = discord.FFmpegPCMAudio(fp.name)

        self.voice = await ctx.author.voice.channel.connect()
        self.voice.play(to_play, after=exit)


def setup(bot):
    bot.add_cog(Sound(bot))