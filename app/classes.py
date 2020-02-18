import requests
from app.constant import *
import random
from app.config import *


class ResponsePy:
    def __init__(self):
        self.ok = [
            "Bien sûr mon poussin ! J'ai une bonne histoire \
        sur cet endroit d'ailleurs !! :D",
            "D'accord.. ma mémoire me joue quelques tours mais je crois \
        que c'est par là bas.. ça me rappelle des souvenirs.. te l'ai\
         je déjà raconter ?",
            "Oh oups ! Je m'endormais ! :) Euh.. alors.. oui.. si je me \
        souviens bien ça me rappelle quelque chose cet endroit !!",
        ]

        self.no = [
            "Que dis-tu mon petit ? Mes oreilles se font vieilles,\
         je n'ai pas compris.. :/",
            "Peux tu un peu préciser ta question? aah... ces jeunes...",
            "Essaie encore.. :)",
        ]

    def send(self, list):
        """Choose a sentence randomly from one of the two lists. the choice of
        a list depends of the request result"""

        return random.choice(list)


class Parser:
    """create object with the sentence of received request user"""

    def __init__(self, value):
        self.input = value

    def ponctuation(self):
        """Delete all punctuation mark from the sentence"""

        PONCTUATION = "?,;.:/!§&~'#{}()[]=+<>&"
        for item in PONCTUATION:
            if item in self.input:
                self.input = self.input.replace(item, " ")
        return self.input

    def list_it(self):
        """Transform sentence into a list. Each word become a list element"""
        self.input = self.input.split()
        return self.input

    def delete_common_words(self):
        """For each element in the list, compare it with a constant list of
        common words. If the element is not in the common words list, add it in
        a thrid list. This will be finally convert into a character string"""

        not_common_words = []
        for item in self.input:
            if item not in STOPWORDS:
                not_common_words.append(item)
        self.input = " ".join(not_common_words)
        print(self.input)
        return self.input


class Map:
    def __init__(self, value):
        self.place = value
        self.url = "https://maps.googleapis.com/maps/api/geocode/json?address="

    def localisation(self):
        """Request a localisation to Google with the sentence cleaned before"""

        r = requests.get(self.url + self.place + "&key=" + key_value)
        data = r.json()
        return data["results"][0]["geometry"]["location"]


class Wiki:
    def __init__(self, coordinates):
        """Thanks to Google coordinates, create an object wiki"""
        self.geo = coordinates
        self.url = "https://fr.wikipedia.org/w/api.php"

    def nearly(self):
        """request to wikipedia to check pages about a place near of google
        coordinates. Select the first result which mean the nearest place"""

        PARAMS = {
            "format": "json",
            "list": "geosearch",
            "gscoord": str(self.geo["lat"]) + "|" + str(self.geo["lng"]),
            "gslimit": "10",
            "gsradius": "10000",
            "action": "query",
        }
        r = requests.get(url=self.url, params=PARAMS)
        data = r.json()
        return data["query"]["geosearch"][0]["pageid"]

    def about(self, page):
        """request to wikipedia. From the page, extract a summary"""

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
