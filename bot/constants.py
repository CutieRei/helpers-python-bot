import json

with open('bot/config.json') as fp:
    data = json.load(fp)

TOKEN = data["TOKEN"]
PREFIXES = data["PREFIXES"]

DISCORDPY_URL = "https://discordpy.readthedocs.io/en/latest/"