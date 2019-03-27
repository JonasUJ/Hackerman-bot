import os
import discord
from discord.ext import commands
from utils import Utils


utils = Utils()
bot = commands.Bot(utils.config['command_prefix'])
utils.bot = bot


@bot.event
async def on_ready():

    # Print something to let us know the bot has started
    print('Logged in as:', bot.user.name)
    print('User id:', bot.user.id)
    print('--------')
    await bot.change_presence(activity=discord.Game(name='{}help'.format(bot.command_prefix), type=0))

@bot.event
async def on_message(message):
    await bot.process_commands(message)

if __name__ == '__main__':

    # Load extensions
    for cog in os.listdir('cogs'):
        name, extension = os.path.splitext(cog)
        if extension == '.py':
            bot.load_extension('cogs.{}'.format(name))

    # Launch bot
    bot.run(utils.config['token'])