import requests

class util:
    def __init__(self, bot):
        self.bot = bot
    def check_name_validity(self, name: str):
        res = requests.get(f'https://osu.ppy.sh/api/get_user?k={self.bot.osu_token}&u={name}').text
        if(res == '[]'):
            return False
        else:
            return True

    def check_map_validity(self, id: str):
        res = requests.get(f'https://osu.ppy.sh/api/get_beatmaps?k={self.bot.osu_token}&b={id}').text
        if(res == '[]'):
            return False
        else:
            return True

    def user_dict(self, user_id):
        
        v = self.check_name_validity(user_id)
        if(v):
            r = requests.get(f'https://osu.ppy.sh/api/get_user?k={self.bot.osu_token}&u={user_id}').json()[0]
            return r
        else:
            raise Exception('This user is not Exists')

    def user_last(self, user_id):
        
        v = self.check_name_validity(user_id)
        if(v):
            r = requests.get(f'https://osu.ppy.sh/api/get_user_recent?k={self.bot.osu_token}&u={user_id}&limit=1').json()[0]
            return r
        else:
            raise Exception('This user is not Exists')

    def best_user_dict(self, user_id):
        
        v = self.check_name_validity(user_id)
        if(v):
            r = requests.get(f'https://osu.ppy.sh/api/get_user_best?k={self.bot.osu_token}&u={user_id}').json()[0]
            return r
        else:
            raise Exception('This user is not Exists')
            
    def get_map(self, map_id):
        
        v = self.check_map_validity(map_id)
        if(v):
            r = requests.get(f'https://osu.ppy.sh/api/get_beatmaps?k={self.bot.osu_token}&b={map_id}').json()[0]
            return r
        else:
            raise Exception('This map is not Exists')



