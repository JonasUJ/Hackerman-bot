import discord
from discord.ext import commands


class basicCog:

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def ping(self, ctx, *, content):
        await ctx.send('Pong')

    
    @commands.command()
    async def exit(self, ctx):
        if ctx.author.id == 1234567890:
            await self.bot.close()
        else:
            await ctx.send('Permission denied')


def setup(bot):
    bot.add_cog(basicCog(bot))