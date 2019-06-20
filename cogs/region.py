import discord
from discord.ext import commands


class Region(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_region(self, region):
        if region == discord.enums.VoiceRegion.eu_central:
            return discord.enums.VoiceRegion.eu_west
        return discord.enums.VoiceRegion.eu_central

    @commands.guild_only()
    @commands.cooldown(2, 30)
    @commands.command()
    async def switch(self, ctx: commands.Context):
        '''
        Switch between the two eu regions
        '''
        try:
            await ctx.guild.edit(region=self.get_region(ctx.guild.region))
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @switch.error()
    async def switch_error(self, ctx: commands.Context, error):
        if type(error) == commands.errors.CommandOnCooldown:
            await ctx.send('Command is on cooldown for up to 30 seconds')
        await ctx.message.add_reaction('\u274C')


def setup(bot):
    bot.add_cog(Region(bot))
