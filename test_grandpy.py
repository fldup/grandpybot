import app.routes as script
import requests

from io import BytesIO

class TestResponse:
    RESPONSE = script.ResponsePy()

    def test_send(self):
        assert type(self.RESPONSE.send(self.RESPONSE.ok)) == str


class TestParser:
    SENTENCE = script.Parser('ceci, est )un ;message avec? trop : de ponctuation !!')

    def test_ponctuation(self):
        assert ',' not in self.SENTENCE.ponctuation()

    def test_listIt(self):
        assert type(self.SENTENCE.listIt()) == list

    def test_deleteCommonWords(self):
        assert type(self.SENTENCE.deleteCommonWords()) == str




FAKE_COORDINATES = {'results' : [{'geometry':{'location': {'lat':0, 'lng' : 0}}}]}

def fake_request_googlemap(*args,**kwargs):
    return TestMap()

class TestMap:
    def json(self):
        return FAKE_COORDINATES

def test_http_return(monkeypatch):
    ZONE = script.Map('Openclassrooms Paris')
    monkeypatch.setattr(requests,'get',fake_request_googlemap)
    assert ZONE.localisation() == FAKE_COORDINATES['results'][0]['geometry']['location']



COORD = script.Wiki({'lat':0, 'lng' : 0})

FAKE_PAGE = {'query':{'geosearch':[{'pageid':'Paris'}]}}
def fake_request_wiki(*args,**kwargs):
    return TestWiki()

class TestWiki:
    def json(self):
        return FAKE_PAGE

def test_nearly_return(monkeypatch):
    monkeypatch.setattr(requests,'get',fake_request_wiki)
    assert COORD.nearly() == FAKE_PAGE['query']['geosearch'][0]['pageid']


FAKE_EXTRACT = {'query': {'pages':{'0':{'extract': 'Paris est la capitale de France'}}}}
def fake_request_extract(*args,**kwargs):
    return TestExtract()

class TestExtract:
    def json(self):
        return FAKE_EXTRACT

def test_about_return(monkeypatch):
    page = 0
    monkeypatch.setattr(requests,'get',fake_request_extract)
    assert COORD.about(page) == FAKE_EXTRACT["query"]["pages"][str(page)]["extract"]
