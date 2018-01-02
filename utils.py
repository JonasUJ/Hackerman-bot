import json
import os
import functools

import aiohttp


class Utils:

    def __init__(self, bot=None):

        # Define standard configs
        # Used if config.json is missing an item
        self.STANDARD = {
            "command_prefix": "&",
            "cogs": {
                
            }
        }

        with open('codeindex.json') as fp:
            self.code_index = json.load(fp)

        self.is_heroku = os.environ.get('IS_HEROKU', None)
        
        def setitems(dic: dict, standard: dict):
            '''Recursivly generate a dictionary from dic with fallback to standard'''

            res = {}
            for k, v in standard.items():
                if isinstance(v, dict):
                    if dic.get(k):
                        res[k] = setitems(dic[k], standard[k])
                    else:
                        res[k] = standard[k]
                else:
                    try:
                        res[k] = dic[k]
                    except KeyError:
                        res[k] = v

            return res

        self.bot = bot

        # Attempt reading config.json
        try:
            with open('config.json') as f:
                self.loaded = json.load(f)
        except (FileNotFoundError, IOError, OSError):
            self.loaded = {}

        self.config = setitems(self.loaded, self.STANDARD)

        # Attempt reading secrets.json and update self.config with the result
        try:
            with open('secrets.json') as f:
                self.secrets = json.load(f)
        except (FileNotFoundError, IOError, OSError):
            raise FileNotFoundError('A "secrets.json" file containing your token etc. is required in this directory')
        else:
            self.config.update(self.secrets)
            if self.is_heroku:
                self.config['token'] = os.environ.get('TOKEN')
                self.config['my_id'] = os.environ.get('MY_ID')
                self.config['wolfram_token'] = os.environ.get('WOLFRAM_TOKEN')

        
    async def run_async(self, sync_func, *args, **kwargs):
        """Run sync func as async"""
        
        nfunc = functools.partial(sync_func, *args, **kwargs)
        res = await self.bot.loop.run_in_executor(None, nfunc)
        return res

    
    def get_language_index(self, language):
        """Lookup the position of language in codeindex.json"""

        for i, iterable in enumerate(self.code_index):
            if language in iterable:
                if i > 35:
                    return i+2
                return i+1
        return None
    

    @classmethod
    async def fetch(cls, url, params={}, mimetype='json'):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, params=params) as r:
                res = await getattr(r, mimetype)()
        return res
