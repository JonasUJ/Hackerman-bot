from datetime import datetime

from bs4 import BeautifulSoup

import discord
from discord.ext import commands
from utils import Utils


url = 'https://politi.dk/coronavirus-i-danmark/foelg-smittespredningen-globalt-regionalt-og-lokalt'

async def fetch_corona():
    resp = await Utils.fetch(url, mimetype='text')
    soup = BeautifulSoup(resp, features='html.parser')
    data = []
    tables = soup.find_all('tbody')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

    return data


class Corona(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils(self.bot)

    async def refresh(self, msg):
        data = await fetch_corona()
        danmark = list(filter(lambda l: l[0] == 'Danmark', data))[0]
        intensiv = list(filter(lambda l: l[0] == 'Hele landet', data))[0]
        globalt = list(filter(lambda l: l[0] == 'Globalt', data))[0]

        emb = discord.Embed(
            title = 'Coronasmitte',
            url = url,
            timestamp = datetime.utcnow(),
        )

        emb.add_field(
            name = 'Smitte i danmark',
            value = f'{danmark[2]} smittede, {danmark[3]} døde, {intensiv[1]} indlagt ({intensiv[2]} på intesiv)',
            inline = False
        )
        emb.add_field(
            name = 'Smitte globalt',
            value = f'{globalt[1]} smittede, {globalt[2]} døde',
            inline = False
        )

        await msg.edit(content='', embed=emb)

    @commands.command()
    async def corona(self, ctx):
        """
        Get updates on COVID-19 in Denmark
        """

        msg = await ctx.send('Getting data...')
        await self.refresh(msg)
        await msg.add_reaction(u"\U0001F504")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if payload.user_id == self.bot.user.id or message.author != self.bot.user or str(payload.emoji) != u"\U0001F504":
            return
        await self.refresh(message)
        await message.remove_reaction(payload.emoji, payload.member)


def setup(bot):
    bot.add_cog(Corona(bot))