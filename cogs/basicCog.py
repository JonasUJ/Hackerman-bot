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


    @commands.is_owner()
    @commands.command(hidden=True)
    async def exit(self, ctx):
        """Unavailable to anyone but me, resets the bot"""

        try:
            await ctx.message.add_reaction('✅')
            await self.bot.close()
        except:
            await ctx.message.add_reaction('❌')


    @commands.is_owner()
    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx, *, expr):
        try:
            await ctx.send(f'```py\n{exec(expr, globals(), locals())}```')
        except Exception as e:
            await ctx.send(str(e))

def setup(bot):
    bot.add_cog(Basic(bot))
