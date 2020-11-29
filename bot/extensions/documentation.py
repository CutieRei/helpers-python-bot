import aiohttp
import zlib
import discord
from io import BytesIO
from discord.ext import commands

from .. import constants

class Documentation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client_session = aiohttp.ClientSession()
        self.inventory = []
        bot.loop.create_task(self.crawl())

    async def crawl(self):
        async with self.client_session.request('GET', constants.DISCORDPY_URL + 'objects.inv') as resp:
            data = await resp.read()
        io = BytesIO(data)
        for _ in range(4):
            io.readline()
        decompressed = zlib.decompress(io.read()).decode()
        for line in decompressed.splitlines():
            name, type_, _, path, *name2 = line.split()
            actual_name = name
            if name2[0] != '-':
                name = ''.join(name2)
            if path.endswith('$'):
                path = constants.DISCORDPY_URL + path.strip('$') + actual_name
            else:
                path = constants.DISCORDPY_URL + path
            self.inventory.append((name, path))
            if name != actual_name:
                self.inventory.append((actual_name, path))
        
    @commands.command()
    async def rtfm(self, ctx: commands.Context, *, query: str) -> None:
        results = []
        for name, path in self.inventory:
            if query.lower() in name.lower():
                results.append((name, path, len(query.replace(name, ''))))
        if not results:
            await ctx.send('Hmmph... couldn\'t find anything for that query')
            return
        description = []
        for name, path, exactness in sorted(results, key=lambda item: item[2]):
            description.append('[{}]({})'.format(name, path))
            if len(description) > 15:
                break
        embed = discord.Embed(title='Results for {}'.format(query), description='\n'.join(description))
        await ctx.send(embed=embed)
        
            
def setup(bot: commands.Bot):
    bot.add_cog(Documentation(bot))    
