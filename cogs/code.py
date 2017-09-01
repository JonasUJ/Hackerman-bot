import re
import traceback
import os
import discord
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from discord.ext import commands
from utils import Utils


class Code:

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

        # RegularExpression for detecting python code markdown
        self.code_expr = re.compile(r'```py\n([^```]+)')

    
    @commands.command()
    async def process(self, ctx, *, to_process):
        '''Process the code passed in to_process and edit ctx.message with output'''

        try:
            # Get code to run
            to_exec = self.code_expr.search(to_process).group(1).encode('utf-8')
        except AttributeError:
            # If the code markdown was improperly formatted
            return

        # Send message confirming that the snippet is being processed
        final_msg = await ctx.send('Processing...\n{}'.format(to_process))

        # Create tempFile and write code to it
        tempFile = NamedTemporaryFile(delete=False)
        tempFile.write(to_exec)
        tempFile.close()

        # Open tempFile with Python
        process = Popen(['python3', tempFile.name], shell=True, stdout=PIPE, stderr=PIPE, bufsize=0)

        # Get output
        out = process.stdout.read().decode('utf-8')
        err = process.stderr.read().decode('utf-8')

        print(process, tempFile.name, out, err, process.communicate())
        with open(tempFile.name) as t:
            print(t.read())

        # Remove tempFile
        os.remove(tempFile.name)

        # Format output
        formatted_output = '```py\n{}{}```'.format(out, err)
        if formatted_output == '```py\n```': formatted_output = '```No output```'
        new_msg = '{}\nOutput:{}'.format(to_process, formatted_output)

        try:
            # Edit message
            await final_msg.edit(content=new_msg)
        except discord.errors.HTTPException:
            await final_msg.edit(content='Failed\n{}'.format(to_process))
        

   
    @commands.command()
    async def eval(self, ctx, *, expr):
        '''Evaluate an expression'''
        pass


def setup(bot):
    bot.add_cog(Code(bot))
