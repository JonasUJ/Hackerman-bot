"""Cog for a discord bot"""

import re
import inspect
from urllib.parse import quote

import discord
from discord.ext import commands
from utils import Utils


class MarkdownCode:
    """Get the language and code of a code section formatted like the following: ```lang\n code```"""

    def __init__(self, code_section: str):
        
        # RegularExpression for detecting language and code 
        self.code_expr = re.compile(r'```(\w*)\n\s*([^```]+)\s*```\s*(\w*)')

        match = self.code_expr.search(code_section)

        try:
            self.lang = match.group(1)
            self.src = match.group(2)
            self.excess = match.group(3)
        except AttributeError:
            self.lang = None
            self.src = None

        
    def __repr__(self):
        return f'<MarkdownCode object: lang={self.lang}, src={self.src}>'


    def __bool__(self):
        return bool(self.lang) and bool(self.src)


class Code:

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)


    @commands.command(aliases=['code', 'r'])
    async def run(self, ctx, *, code: MarkdownCode, stdin=""):
        """
        Run code for various languages using http://rextester.com
        Look at their site for a full list of available languages
        or go to https://github.com/JonasUJ/Hackerman-bot/codeindex.json

        Usage:
        Code is formatted using discords built in markdown support
        run \`\`\`language
        code
        \`\`\` "stdin input"
        """

        if not code:
            await ctx.message.add_reaction('❌')
            return await ctx.send(f'Code formatted incorrectly, try `{self.bot.command_prefix}help run`')

        lang = self.utils.get_language_index(code.lang)
        if not lang:
            await ctx.message.add_reaction('❌')            
            return await ctx.send(f'Language `{code.lang}` not recognized')

        stdin = code.excess
        
        with ctx.typing():
            resp = await self.utils.fetch(f'http://rextester.com/rundotnet/api?LanguageChoice={lang}&Program={quote(code.src)}&Input={quote(stdin)}')

        emb = discord.Embed(title=f"Ran program with language {code.lang}", description=resp['Stats'])

        for k, v in resp.items():
            if k == "Stats":
                continue
            if v:
                emb.add_field(name=k, value=f'```{code.lang}\n{v}```')

        try:
            await ctx.send(embed=emb)
            await ctx.message.add_reaction('✅')
        except discord.errors.HTTPException:
            await ctx.message.add_reaction('❌')
            return await ctx.send('Failed, output length too high.')


    @commands.command()
    async def src(self, ctx, *, cmd: str = None):
        """
        Get the source code of a command for whatever reason
        """

        if not cmd:
            await ctx.send('https://github.com/JonasUJ/Hackerman-bot')
            return await ctx.message.add_reaction('❌')

        command = self.bot.get_command(cmd)
        if not command:
            await ctx.send('No such command')
            return await ctx.message.add_reaction('❌')

        src = command.callback.__code__
        lines, firstlineno = inspect.getsourcelines(src)
        lines = ''.join(lines).replace('```', '\`\`\`')

        await ctx.send(f'```py\n{lines}```')
        return await ctx.message.add_reaction('✅')


def setup(bot):
    bot.add_cog(Code(bot))
