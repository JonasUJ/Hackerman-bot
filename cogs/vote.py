import asyncio
import time

import discord
from discord.ext import commands
from utils import Utils


class Vote:

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Found no member with that name (usernames are case-sensitive)')
    
    async def end_vote(self, ctx, msgid):
        yes, no = 1, 1
        msg = await ctx.channel.get_message(msgid)

        for reac in msg.reactions:
            if str(reac) == '\u2705':
                yes = reac.count
            elif str(reac) == '\u274C':
                no = reac.count
        
        if yes > no:
            await ctx.send('The majority votes yes \u2705')
            return True
        elif no > yes:
            await ctx.send('The majority votes no \u274C')
            return False
        else:
            await ctx.send('It\'s a draw')
            return False

    @commands.command()
    async def vote(self, ctx, *, topic):

        async def timeout(timeout_time, ctx, msg):
            now = time.time()
            end = now + timeout_time
            await self.bot.wait_until_ready()

            while now < end:
                if not round(now) % 5:
                    await msg.edit(content=f'{topic.capitalize()} - Countdown: {round(end - now)}')
                await asyncio.sleep(0.5)
                now = time.time()
            await msg.edit(content=f'{topic.capitalize()}')
            await self.end_vote(ctx, msg.id)

        msg = await ctx.send(f'{topic.capitalize()} - Countdown: 20')
        await msg.add_reaction('\u2705')
        await msg.add_reaction('\u274C')
        self.bot.loop.create_task(timeout(20, ctx, msg))


    @commands.command()
    async def votekick(self, ctx, *, user:commands.MemberConverter):
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send('You do not have permission to kick members')

        async def kick_timeout(timeout_time, ctx, msg):
            now = time.time()
            end = now + timeout_time
            await self.bot.wait_until_ready()

            while now < end:
                if not round(now) % 5:
                    await msg.edit(content=f'Kick {user}? Countdown: {round(end - now)}')
                await asyncio.sleep(0.5)
                now = time.time()
            await msg.edit(content=f'Kick {user}?')

            if await self.end_vote(ctx, msg.id):
                await ctx.send('not actually kicking, currently just testing...')

        msg = await ctx.send(f'Kick {user}? Countdown: 20')
        await msg.add_reaction('\u2705')
        await msg.add_reaction('\u274C')
        self.bot.loop.create_task(kick_timeout(20, ctx, msg))


def setup(bot):
    bot.add_cog(Vote(bot))