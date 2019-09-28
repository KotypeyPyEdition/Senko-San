# osu! API wrapper written in aiohttp
# © AliceLostInDarkness
#Remaked to Gatari by Kotypey
from aiohttp import ClientSession


class Client:
  def __init__(self, token: str):
    """
    Initialize the class.
    
    Args
    ----
    token: :class:`str` Your secret auth key
    """
    self.token = token
    self.base_url = "https://osu.ppy.sh/api/"
    self.gatari_api = 'https://api.gatari.pw/user/'
    self.scored_uri = "https://api.gatari.pw/user/scores/"
    self.session = None
  
  
  async def get_session(self):
    """
    Get current aiohttp client session if exists;
    If not, create one.
    """
    if not self.session:
      self.session = ClientSession()
      
    return self.session
  
  
  async def validate_player(self, playername: str) -> bool:
    """
    Validate player on the osu! server.
    
    Args
    ----
    playername: :class:`str` Player's nickname
    """
    session = await self.get_session()
    
    async with session.get("https://api.gatari.pw/user/stats?u={}&mode=0".format(playername)) as response:
      data = await response.json()
    
    if not data:
      return False
    return True
    
  
 
    
  
  async def get_player(self, playername: str, mode=0) -> dict:
    """
    Fetch player info from osu! servers.
    
    Args
    ----
    playername: :class:`str` Player's nickname
    """
    session = await self.get_session()
    
    async with session.get(self.gatari_api + "stats?u={0}&mode={1}".format(playername, mode)) as response:
      data = await response.json()
      
    return data['stats']
  
  
  async def get_best_user(self, playername: str) -> dict:
    """
    Fetch player's best.
    
    Args
    ----
    playername: :class:`str` Player's nickname
    """
    player = self.get_player(playername)
    session = await self.get_session()
    player = await self.get_player(playername)
    url = self.scored_uri + "best?id={0}&l=1".format(player['id'])
    async with session.get(url) as response:
      data = await response.json()
      
    return data



  async def get_recent_user(self, playername: str, limit=1,mode=0) -> dict:
    """
    Fetch player's recent.
    
    Args
    ----
    playername: :class:`str` Player's nickname
    """
    session = await self.get_session()

    player = await self.get_player(playername)
    url = self.scored_uri + "recent?id={0}&l={1}&p=1&mode={2}&f=1".format(player['id'],limit, mode)
    async with session.get(url) as response:
      data = await response.json()
      
    return data
  
  async def get_beatmap(self, map_id: int) -> dict:
    """
    Fetch beatmap from the osu! servers.
    
    Args
    ----
    map_id: :class:`int` Beatmap ID
    """
    session = await self.get_session()
    
    async with session.get(self.base_url + "get_beatmaps?k={0}&b={1}".format(self.token, map_id)) as response:
      data = await response.json()
    
    return data

  async def get_profile(self, playerbane: str) -> dict:
    session = await self.get_session()

    async with session.get('http://api.gatari.pw/users/get?u={}&mode=0'.format(playerbane)) as res:
      response = await res.json()

    return response['users'][0]


  
    
    
