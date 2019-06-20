import discord
from discord.ext import commands


class Region(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_region(self, region):
        if region == discord.enums.VoiceRegion.eu_central:
            return discord.enums.VoiceRegion.eu_west
        return discord.enums.VoiceRegion.eu_central

    @commands.command(aliases=['imprison', 'jail'])
    @commands.guild_only()
    @commands.has_any_role()
    async def newregion(self, ctx: commands.Context, member: commands.MemberConverter):
        try:
            await ctx.guild.edit(region=self.get_region(ctx.guild.region))
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')


def setup(bot):
    bot.add_cog(Region(bot))
