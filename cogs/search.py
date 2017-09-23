"""Cog for a discord bot"""

from urllib.parse import quote

import wolframalpha
import discord
from discord.ext import commands
from utils import Utils


async def definition_urban(word):
    """
    Return definition of word from UrbanDictionary in a dictionary
    
    Returns a dict object:

    * definition is the definition of word
    * status
        * status 'ok' means the operation was successful
        * status 'no_result' means that there's no definition for the word
        * status 'error' means that the connection couldn't be established
    * example is word used in a sentence
    * link is the source
    * word is the title of the result
    """

    res = {'definition': '', 'example': '', 'status': 'ok', 'link': '', 'word': ''}
    try:
        dic = await Utils.fetch('http://api.urbandictionary.com/v0/define?term={term}'.format(term=quote(word)))
        if dic['result_type'] == 'no_results':
            res['status'] = 'no_result'
        else:
            res['definition'] = dic['list'][0]['definition']
            res['example'] = dic['list'][0]['example']
            res['link'] = dic['list'][0]['permalink']
            res['word'] = dic['list'][0]['word']
    except:
        res['status'] = 'error'
    finally:
        return res


async def definition_kym(meme):
    """
    Return definition of a meme from KnowYourMeme in a dictionary

    Returns a dict object:
    * summary the description of the meme
    * status
        * status 'ok' means the request succeeded
        * status 'error' means the request failed
    * img_url is the link of the associated with the meme
    * name is the name of the meme
    * link is the uri leading to the source
    """

    res = {'summary': '', 'status': 'ok', 'img_url': '', 'name': '', 'link': ''}
    try:
        resp = await Utils.fetch('http://rkgk.api.searchify.com/v1/indexes/kym_production/instantlinks?query={term}&fetch=*'.format(term=meme))
        res['summary'] = resp['results'][0]['summary']
        res['img_url'] = resp['results'][0]['icon_url']
        res['name'] = resp['results'][0]['name']
        res['link'] = 'https://www.knowyourmeme.com{}'.format(resp['results'][0]['url'])
    except:
        res['status'] = 'error'
    finally:
        return res


class Search:
    """Search for something using services such as `UrbanDictionary` or `KnowYourMeme`"""

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)
        self.wolfram_client = wolframalpha.Client(self.utils.config['wolfram_token'])


    @commands.group(invoke_without_command=True, description='Define word/term/meme etc.', aliases=['def', 'd', 'definition'])
    async def define(self, ctx):
        """
        Define something with a given service

        "define word foobar"
            Finds the definition of `foobar` on UrbanDictionary

        "define meme foobar"
            Finds the summary of a meme on KnowYourMeme

        etc.
        """

        await ctx.message.add_reaction('❌')
        await ctx.send('None or invalid source supplied, try `{}help define`'.format(self.bot.command_prefix))


    @define.command(description='Find word definition on UrbanDictionary', aliases=['ud', 'urban', 'urbandictionary', 'w'])
    async def word(self, ctx, *, word: str):
        """Look up the definition of a word or sentence on UrbanDictionary"""
        
        async with ctx.typing():
            word = word.lower()
            resp = await definition_urban(word)

            if resp['status'] == 'error':
                await ctx.message.add_reaction('❌')
                return await ctx.send('Unable to connect to UrbanDictionary')

            elif resp['status'] == 'no_result':
                await ctx.message.add_reaction('❌')
                return await ctx.send('No definition for `{}`'.format(word))

            elif resp['status'] == 'ok':
                defined = (resp['definition'] + ('\n\n_{}_'.format(resp['example'].strip('\n').replace('*', r'\*')) if resp['example'] else ''))
                if len(defined) >= 2048:
                    defined = defined[:2044] + '..._'
                emb = discord.Embed(
                    title='Definition for `{word}`'.format(word=resp['word']),
                    description=defined,
                    url=resp['link'])
                await ctx.message.add_reaction('✅')
                return await ctx.send(embed=emb)


    @define.command(description='Memes from KnowYourMeme', aliases=['m', 'kym', 'knowyourmeme'])
    async def meme(self, ctx, *, meme: str):
        """Find a meme on KnowYourMeme and display it in chat"""

        async with ctx.typing():
            meme = meme.lower()
            resp = await definition_kym(meme)

            if resp['status'] == 'error':
                await ctx.message.add_reaction('❌')
                return await ctx.send('No entry for `{}`'.format(meme))
            
            elif resp['status'] == 'ok':
                summarised = resp['summary']
                if len(summarised) >= 2048:
                    summarised = summarised[:2045] + '...'
                emb = discord.Embed(
                    title='`{name}`'.format(name=resp['name']),
                    description=summarised,
                    url=resp['link'])
                emb.set_image(url=resp['img_url'])

                await ctx.message.add_reaction('✅')
                return await ctx.send(embed=emb)


    @commands.group(invoke_without_command=True, aliases=['s', 'find'])
    async def search(self, ctx):
        """Find results from services like Wolfram|Alpha"""

        await ctx.message.add_reaction('❌')
        await ctx.send('None or invalid source supplied, try `{}help search`'.format(self.bot.command_prefix))


    @search.command(aliases=['wa', 'wolframalpha'])
    async def wolfram(self, ctx, *, term):
        """Send the result of a Wolfram|Alpha search for 'term'"""

        async with ctx.typing():
            resp = await self.utils.run_async(self.wolfram_client.query, term)

            if resp.get('@success') == 'false':
                await ctx.message.add_reaction('❌')
                return await ctx.send('No result for `{}`, try rephrasing your search (eg. `hc andersen` -> `h.c. andersen`)'.format(term))

            emb = discord.Embed(
                title=list(resp.pods)[0]['subpod']['plaintext']
            )

            for pod in resp.pods:
                if pod['@id'] == 'Input':
                    continue
                subpod = pod['subpod']
                if isinstance(subpod, list):
                    for entry in subpod:
                        emb.add_field(
                            name=pod['@title'],
                            value=entry['plaintext']
                        )
                elif isinstance(subpod, dict):
                    if subpod['plaintext']:
                        emb.add_field(
                            name=pod['@title'],
                            value=subpod['plaintext']
                        )
                    elif not emb.image:
                        emb.set_image(url=subpod['img']['@src'])

            try:
                await ctx.message.add_reaction('✅')
                return await ctx.send(embed=emb)
            except:
                await ctx.message.add_reaction('❌')
                return await ctx.send('Unable to send result (probably due to message charater limit)')


def setup(bot):
    bot.add_cog(Search(bot))