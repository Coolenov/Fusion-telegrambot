import requests
from dataclasses import dataclass
import json
import datetime


@dataclass
class Tag:
    text: str

@dataclass
class Content:
    Id:                 int
    Title:              str
    Link:               str
    Description:        str
    ImageUrl:          str
    Source:             str
    PublishingTime:    int

@dataclass
class Source:
    name:str


class Nax:
    def __init__(self):
        self.session = requests.Session()
        self.baseUrl = "http://127.0.0.1:10000"
    
    def _formPublishingTime(self, timeStamp:int)->datetime:
        return datetime.datetime.fromtimestamp(timeStamp)

    def _createContentFromResp(self,resp:json)->Content:
        resp = resp["content"]
        return Content(resp['Id'], resp['Title'], resp['Link'], resp['Description'], 
                        resp['Image_url'],resp['Source'],self._formPublishingTime(resp['Publishing_time']))

    def GetTextForTelegramMessage(self,content:Content)->str:
        return f'<b>{content.Title}</b>\n\n{content.Description}\n{content.PublishingTime}'

    def GetLastContentBySource(self,source:str)->Content:
        resp = self.session.post(f"{self.baseUrl}/content/source",data = {"source":source})
        resp = resp.json()
        return self._createContentFromResp(resp)

    def GetNextContent(self,post_id:str)->Content:
        resp = self.session.post(f"{self.baseUrl}/next",data = {"id":post_id})

        resp = resp.json()
        if resp["error"] == True:
            return None
        return self._createContentFromResp(resp)

    def GetPreviousContent(self,post_id:str)->Content:
        resp = self.session.post(f"{self.baseUrl}/previous",data = {"id":post_id})
        resp = resp.json()
        return self._createContentFromResp(resp)

    def GetSources(self)->list[str,...]:
        resp = self.session.get(f"{self.baseUrl}/sources")
        resp = resp.json()
        sources = resp["content"]
        return sources







