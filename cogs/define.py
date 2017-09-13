import os
import requests
import discord
from discord.ext import commands
from urllib.parse import quote
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


class Define:
    """Define a term using services such as `UrbanDictionary` or `KnowYourMeme`"""

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

    @commands.group(invoke_without_command=True, description='Define a word/term/meme/etc.', aliases=['def', 'd', 'definition'])
    async def define(self, ctx):
        """Define something"""

        await ctx.send('No source supplied, try `{}help define`'.format(self.bot.command_prefix))


    @define.command(description='Find word definition on UrbanDictionary', aliases=['ud', 'urban', 'urbandictionary', 'w'])
    async def word(self, ctx, *, word):
        """Look up the definition of a word or sentence on UrbanDictionary"""
        
        resp = await definition_urban(word)

        if resp['status'] == 'error':
            return await ctx.send('Unable to connect to UrbanDictionary')

        elif resp['status'] == 'no_result':
            return await ctx.send('No definition for `{}`'.format(word))

        elif resp['status'] == 'ok':
            defined = (resp['definition'] + ('\n\n_{}_'.format(resp['example'].strip('\n').replace('*', r'\*')) if resp['example'] else ''))
            if len(defined) >= 2048:
                defined = defined[:2044] + '..._'
            emb = discord.Embed(
                title='Definition for `{word}`'.format(word=resp['word']),
                description=defined,
                url=resp['link'])
            return await ctx.send(embed=emb)


    @define.command(description='Memes from KnowYourMeme')
    async def meme(self, ctx, *, meme):
        """Find a meme on KnowYourMeme and display it in chat"""

        resp = await definition_kym(meme)

        if resp['status'] == 'error':
            return await ctx.send('No entry for `{}`'.format(meme))
        
        elif resp['status'] == 'ok':
            emb = discord.Embed(
                title='`{name}`'.format(name=resp['name']),
                description=resp['summary'],
                url=resp['link'])
            emb.set_image(url=resp['img_url'])
            return await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Define(bot))