"""Cog for a discord bot, uses a discord.VoiceClient to play sounds"""

from tempfile import TemporaryFile

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


    @commands.command()
    async def play(self, ctx, *args):
        """Play a `mp3` file that was sent over discord as an attachment"""

        if not ctx.author.voice:
            return await ctx.send("You're not connected to a voice channel.")

        with TemporaryFile() as fp:
            attfile = await ctx.message.attachments[0].save(fp)
            to_play = discord.PCMAudio(attfile)

            voice = await ctx.author.voice.channel.connect()
            voice.play(to_play)
            


def setup(bot):
    bot.add_cog(Sound(bot))