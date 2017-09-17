"""Cog for a discord bot, uses a discord.VoiceClient to play sounds"""

import asyncio
from tempfile import NamedTemporaryFile

import discord
from discord.ext import commands
from utils import Utils


if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


class Sound:
    """Different commands for playing sounds"""

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)
        self.voice_clients = list()


    def disconnect(self, voice_index):
        """Disconnect from VoiceChannel"""

        coro = self.voice_clients.pop(voice_index).disconnect()
        fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        fut.result()


    @commands.command()
    async def play(self, ctx, *, args=None):
        """Play a `mp3` file that was sent over discord as an attachment"""

        if not ctx.author.voice:
            return await ctx.send("You're not connected to a voice channel.")

        with NamedTemporaryFile(delete=False) as fp:
            await ctx.message.attachments[0].save(fp)
        to_play = discord.FFmpegPCMAudio(fp.name)

        voice = await ctx.author.voice.channel.connect()
        self.voice_clients.append(voice)
        voice.play(to_play, after=lambda: self.disconnect(self.voice_clients.index(voice)))


def setup(bot):
    bot.add_cog(Sound(bot))