import os
import discord
from discord.ext import commands
from utils import Utils


class Basic:

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

    
    @commands.command(description='Say Pong.')
    async def ping(self, ctx):
        """Check if the bot is alive be making it say Pong."""

        await ctx.message.add_reaction('✅')
        await ctx.send('Pong')

    
    @commands.command(description='Unavailable')
    async def exit(self, ctx):
        """Unavailable to anyone but me, resets the bot"""

        if str(ctx.author.id) == self.utils.config['my_id']:
            await ctx.message.add_reaction('✅')
            await self.bot.close()
        else:
            await ctx.message.add_reaction('❌')


def setup(bot):
    bot.add_cog(Basic(bot))