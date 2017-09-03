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

        # Put in thread that terminates the script after 10 seconds
        to_exec = """def _timeOut(): import time; time.sleep(10)
import threading; t = threading.Thread(target=_timeOut); t.daemon = True; t.start(); t.join(); raise TimeoutError('Process took to long to complete'); {}""".format(to_exec)

        # Send message confirming that the snippet is being processed
        final_msg = await ctx.send('Processing...')

        with stdoutIO() as s:
            try:
                exec(to_exec, dict(), dict())
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
    async def eval(self, ctx, *, expr):
        '''Evaluate an expression'''
        pass


def setup(bot):
    bot.add_cog(Code(bot))
