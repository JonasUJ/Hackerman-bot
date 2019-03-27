import os
from PIL import Image
from tempfile import NamedTemporaryFile

import discord
from discord.ext import commands
from utils import Utils


class Colour(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

    
    @commands.command(aliases=['color', 'c', 'hex'])
    async def colour(self, ctx, hex_value):
        """
        Print a image with one colour, 'hex_value'
        Takes a hex value like '#7289DA'
        """
        try:
            img = Image.new('RGB', (200, 200), tuple(int(hex_value.strip('#')[i:i+2], 16) for i in (0, 2, 4)))
        except ValueError:
            return await ctx.message.add_reaction('❌')

        with NamedTemporaryFile(suffix='.png', delete=False) as fp:
            img.save(fp, 'PNG')

        await ctx.send(file=discord.File(fp.name))
        await ctx.message.add_reaction('✅')
        os.remove(fp.name)

def setup(bot):
    bot.add_cog(Colour(bot))