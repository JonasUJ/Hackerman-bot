"""Cog for a discord bot"""

import re
import sys
import contextlib
from io import StringIO

import discord
from discord.ext import commands
from utils import Utils


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


class Code:

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

        # RegularExpression for detecting python code markdown
        self.code_expr = re.compile(r'```(\w*)\s*([^```]+)\s*```')

    
    @commands.command(aliases=['py', 'code'])
    async def process(self, ctx, *, to_process):
        '''Process the python code passed in and output everything from stdout and stderr'''

        try:
            # Get code to run
            to_exec = self.code_expr.search(to_process).group(1)
        except AttributeError:
            # If the code markdown was improperly formatted
            return

        async with ctx.typing():
            with stdoutIO() as s:
                try:
                    await self.utils.run_async(exec, to_exec, dict(), dict())
                except Exception as e:
                    print(str(type(e)).replace('class ', ''), '\n', e.__str__())
        
        out = s.getvalue()

        # Format output
        formatted_output = '```py\n{}```'.format(out)
        if formatted_output == '```py\n```': 
            formatted_output = '```No output```'
        new_msg = 'Output:{}'.format(formatted_output)

        try:
            # Edit message
            await ctx.send(new_msg)
        except discord.errors.HTTPException:
            await ctx.send('Failed, output length too high.\n{}'.format(to_process))
        

   
    @commands.command(aliases=['calc', 'calculate', 'evaluate'])
    async def eval(self, ctx, *, expr: str):
        '''Evaluate an expression'''
    
        expr = expr.strip('`')

        async with ctx.typing():
            # Process expr
            try:
                output = await self.utils.run_async(eval, expr)
            except:
                return await ctx.send('Something is formatted incorrectly')

        try:
            # Edit message
            await ctx.send('`{} = {}`'.format(expr, output))
        except discord.errors.HTTPException:
            await ctx.send('Failed, output length too high.\n{}'.format(expr))

    
    @commands.command()
    async def rex(self, ctx, *, code):
        
        async with ctx.typing():
            pass


def setup(bot):
    bot.add_cog(Code(bot))
