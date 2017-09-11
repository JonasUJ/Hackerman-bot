import os
import requests
import discord
from discord.ext import commands
from urllib.parse import quote
from utils import Utils


def definition(word):
    """
    Return definition of word from UrbanDictionary
    
    Returns a dict object
    status 'ok' means the operation was successful
    status 'no_result' means that there's no definition for the word
    status 'error' means that the connection couldn't be established
    """

    res = {'definition': '', 'example': '', 'status': 'ok', 'link': ''}
    try:
        feed = requests.get('http://api.urbandictionary.com/v0/define?term={term}'.format(term=quote(word)))
        dic = feed.json()
        if dic['result_type'] == 'no_results':
            res['status'] = 'no_result'
        else:
            res['definition'] = dic['list'][0]['definition']
            res['example'] = dic['list'][0]['example']
            res['link'] = dic['list'][0]['permalink']
    except:
        res['status'] = 'error'
    finally:
        return res


class Define:

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

    
    @commands.command(description='Find word definition on UrbanDictionary')
    async def define(self, ctx, *, word):
        """Look up the definition of a word or sentence on UrbanDictionary"""
        
        resp = await self.utils.run_async(definition, word)

        if resp['status'] == 'error':
            return await ctx.send('Unable to connect to UrbanDictionary')

        elif resp['status'] == 'no_result':
            return await ctx.send('No definition for `{}`'.format(word))

        elif resp['status'] == 'ok':
            emb = discord.Embed(
                title='Definition for `{word}`'.format(word=word),
                description='{definition}\n\n*{example}*'.format(definition=resp['definition'], example=resp['example']),
                url=resp['link'])
            return await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Define(bot))