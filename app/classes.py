import requests
from app.constant import *
import random

class ResponsePy:
    def __init__(self):
        self.ok = ["Bien sûr mon poussin ! J'ai une bonne histoire \
        sur cet endroit d'ailleurs !! :D",
        "D'accord.. ma mémoire me joue quelques tours mais je crois \
        que c'est par là bas.. ça me rappelle des souvenirs.. te l'ai\
         je déjà raconter ?",
        "Oh oups ! Je m'endormais ! :) Euh.. alors.. oui.. si je me \
        souviens bien ça me rappelle quelque chose cet endroit !!"]

        self.no = ["Que dis-tu mon petit ? Mes oreilles se font vieilles,\
         je n'ai pas compris.. :/",
        "Peux tu un peu préciser ta question? aah... ces jeunes...",
        "Essaie encore.. :)"]


    def send (self,list):
        return random.choice(list)




class Parser:
    """docstring for userRequest."""

    def __init__(self, value):
        self.input = value


    def ponctuation(self):
        PONCTUATION = "?,;.:/!§&~'#{}()[]=+<>&"
        for item in PONCTUATION:
            if item in self.input:
                self.input = self.input.replace(item,' ')
        return self.input


    def listIt(self):
        self.input = self.input.split()
        return self.input


    def deleteCommonWords(self):
        notCommonWords = []
        for item in self.input:
            if item not in STOPWORDS:
                notCommonWords.append(item)
        self.input = ' '.join(notCommonWords)
        print(self.input)
        return self.input




class Map():
    def __init__(self, value):
        self.place = value
        self.url = 'https://maps.googleapis.com/maps/api/geocode/json?address='


    def localisation(self):
        r = requests.get(self.url + self.place +
        '&key=' + 'AIzaSyBAjiUDijQmWRHnfAKHWZcRsZBeQSz12cY')
        data = r.json()
        return data['results'][0]['geometry']['location']




class Wiki():
    def __init__(self,coordinates):
        self.geo = coordinates
        self.url = "https://fr.wikipedia.org/w/api.php"


    def nearly(self):
        PARAMS = {
            "format": "json",
            "list": "geosearch",
            "gscoord": str(self.geo['lat']) + '|' + str(self.geo['lng']),
            "gslimit": "10",
            "gsradius": "10000",
            "action": "query"
        }
        r = requests.get(url = self.url, params = PARAMS)
        data = r.json()
        return data['query']['geosearch'][0]['pageid']



    def about(self,page):
        PARAMS = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": "1",
            "explaintext": "1",
            "indexpageids": 1,
            "exsentences": "3",
            "pageids": page,
        }
        r = requests.get(url=self.url, params=PARAMS)
        data = r.json()
        summary = data["query"]["pages"][str(page)]["extract"]
        return summary
