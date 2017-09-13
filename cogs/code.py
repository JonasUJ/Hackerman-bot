import re
import sys
import os
import discord
import contextlib
from io import StringIO
from subprocess import run, Popen, PIPE
from tempfile import NamedTemporaryFile
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
        self.code_expr = re.compile(r'```py\n([^```]+)')

    
    @commands.command(aliases=['py', 'code'])
    async def process(self, ctx, *, to_process):
        '''Process the python code passed in and output everything from stdout and stderr'''

        try:
            # Get code to run
            to_exec = self.code_expr.search(to_process).group(1)
        except AttributeError:
            # If the code markdown was improperly formatted
            return

        # Send message confirming that the snippet is being processed
        final_msg = await ctx.send('Processing...')

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
            await final_msg.edit(content=new_msg)
        except discord.errors.HTTPException:
            await final_msg.edit(content='Failed, output length too high.\n{}'.format(to_process))
        

   
    @commands.command()
    async def eval(self, ctx, *, expr: str):
        '''Evaluate an expression'''
    
        expr = expr.strip('`')
        
        # Confirm the command was recieved
        final_msg = await ctx.send('Processing...')

        # Process expr
        try:
            output = await self.utils.run_async(eval, expr)
        except:
            await final_msg.edit(content='Something is formatted incorrectly')

        try:
            # Edit message
            await final_msg.edit(content='`{} = {}`'.format(expr, output))
        except discord.errors.HTTPException:
            await final_msg.edit(content='Failed, output length too high.\n{}'.format(expr))


def setup(bot):
    bot.add_cog(Code(bot))
