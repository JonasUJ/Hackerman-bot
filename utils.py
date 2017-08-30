import json

class Utils:

    def __init__(self, bot=None):

        # Define standard configs
        # Used if config.json is missing an item
        self.STANDARD = {
            "command_prefix": "|",
            "cogs": {
                
            }
        }
        
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
