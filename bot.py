import os
import discord
from discord.ext import commands
from utils import Utils

is_heroku = os.environ.get('IS_HEROKU', None)

utils = Utils()
bot = commands.Bot(utils.config['command_prefix'])
utils.bot = bot


@bot.event
async def on_ready():

    # Print something to let us know the bot has started
    print('Logged in as:', bot.user.name)
    print('User id:', bot.user.id)
    print('--------')

if __name__ == '__main__':

    # Load extensions
    for cog in os.listdir('cogs'):
        name, extension = os.path.splitext(cog)
        if extension == '.py':
            bot.load_extension('cogs.{}'.format(name))

    # Launch bot
    if is_heroku:
        bot.run(os.environ.get('TOKEN', None))
    else:
        bot.run(utils.config['token'])
