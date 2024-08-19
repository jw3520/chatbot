import requests
import json
class DataFetcher:
    def __init__(self, character, message):
        self.character = character
        self.message = message
        pass
    
    def get_reply(self):
        url = f"http://127.0.0.1:8888/chatinmovie/"

        param = {"character": self.character, "msg": self.message}
        res = requests.post(url, json=param)
        print(json.loads(res.content)['history'])
        rawdata = json.loads(res.content)['reply']
        print(rawdata)
        return rawdata