from bot import constants
from discord.ext import commands

bot = commands.Bot(command_prefix=constants.PREFIXES)

bot.load_extension('bot.extensions.documentation')

bot.run(constants.TOKEN)