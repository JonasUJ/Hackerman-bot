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
        '''Process the code passed in to_process and edit ctx.message with output'''

        try:
            # Get code to run
            to_exec = self.code_expr.search(to_process).group(1)
        except AttributeError:
            # If the code markdown was improperly formatted
            return

        # Send message confirming that the snippet is being processed
        final_msg = await ctx.send('Processing...')

        err = ''

        with stdoutIO() as s:
            try:
                exec(to_exec, dict(), dict())
            except Exception as e:
                err = ''
                print(str(type(e)).replace('class ', ''), '\n', e.__str__())
        
        out = s.getvalue()

        # Format output
        formatted_output = '```xml\n{}{}```'.format(out, err)
        if formatted_output == '```xml\n```': 
            formatted_output = '```No output```'
        new_msg = 'Output:{}'.format(formatted_output)

        try:
            # Edit message
            await final_msg.edit(content=new_msg)
        except discord.errors.HTTPException:
            await final_msg.edit(content='Failed, output length too high.\n{}'.format(to_process))
        

   
    @commands.command()
    async def eval(self, ctx, *, expr):
        '''Evaluate an expression'''
        pass


def setup(bot):
    bot.add_cog(Code(bot))
