import asyncio
import discord
import config
from aiohttp import ClientSession
from discord.ext import commands
from colorama import init, Fore

init()

class RknBot(commands.Bot):

  def __init__(self, *args, **kwargs):
    
    super().__init__(
      *args, **kwargs
    )

    self.load()

    self.blacklisted_cache = {}
  
  async def in_blacklist(self, ctx):

    if not self.blacklisted_cache:
    
      async with self.session.get("http://naomi.fun:8080/api/blacklist") as response:

        response = await response.json()
      
      self.blacklisted_cache = response
    
    return not ctx.author in self.blacklisted_cache

  async def ref(self):

    await self.wait_until_ready()

    while not self.is_closed():

      async with self.session.get(config.lavalink_url):
    
        print('Request sent!')

      await asyncio.sleep(60)

  def load(self):

    self.add_check(
      self.in_blacklist
    )

    self.remove_command('help')
    
    modules = (
      'cogs.emotes',
      'cogs.music', 
      'cogs.admin', 
      'cogs.user',
      'jishaku',
      'cogs.utils',
      'cogs.events',
      'cogs.leveling',
      'cogs.exp',
      'cogs.social',
      'cogs.mod',
      'cogs.rpg',
      'cogs.textutils',
      'cogs.nsfw',
      'cogs.osu'
    )

    for i in modules:
      
      try:

        self.load_extension(i)
        
        print(f'{Fore.BLUE}[Cogs/Info] {Fore.GREEN}{i} {Fore.RED}loaded.')
      
      except Exception as error:

        print(f'{Fore.RED}[Cogs/Error] {Fore.GREEN}{i} {Fore.RED}cannot be loaded!\n{error}')
            
            
  async def on_ready(self):
    
    await self.change_presence(
      activity=discord.Streaming(
        name=f"{config.prefix}help to help", 
        url="https://twitch.tv/smallbabytape0"
      )
    )

    self.session = ClientSession(
      loop=self.loop
    )

    self.loop.create_task(
      self.ref()
    )
    
    print(f"{Fore.BLUE}[Discord/Info] {Fore.RED}Im ready for user login: {Fore.GREEN}{super().user} {Fore.RESET}")
    
  async def on_disconnect(self):
    print(f"{Fore.RED}[Socket/WARN] {Fore.YELLOW}Socket Disconnected")
    
  async def on_connect(self):
    print(f"{Fore.BLUE}[Socket/Info] {Fore.RED}Socket connected")
  
  def run(self, token: str):

    super().run(
      token
    )

if __name__ == "__main__":

  bot = RknBot(
    command_prefix=commands.when_mentioned_or(
      config.prefix
    ),
    case_insensitive=True
  ).run(
    config.token
  )



