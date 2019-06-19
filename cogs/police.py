import discord
from discord.ext import commands
from utils import Utils


class Police(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Found no member with that name (usernames are case-sensitive)')

    @commands.has_role("Police")
    @commands.command(aliases=['imprison', 'jail'])
    async def arrest(self, ctx, member: commands.MemberConverter):
        try:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name="Prisoner"))
            await member.move_to(discord.utils.get(ctx.guild.channels, name="Jail"))
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.has_role("Police")
    @commands.command(aliases=['free', 'unjail'])
    async def pardon(self, ctx, member: commands.MemberConverter):
        try:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Prisoner"))
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')


def setup(bot):
    bot.add_cog(Police(bot))
