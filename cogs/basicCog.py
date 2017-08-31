import os
import discord
from discord.ext import commands
from utils import Utils


class basicCog:

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong')

    
    @commands.command()
    async def exit(self, ctx):
        if ctx.author.id == self.utils.config['my_id']:
            await self.bot.close()
        else:
            await ctx.send('Permission denied')


def setup(bot):
    bot.add_cog(basicCog(bot))