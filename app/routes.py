from flask import render_template, flash, request, jsonify
from app import app
from app.classes import *

# <script>alert('Il y a une faille XSS')</script> ???


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        #reception du json et transformation en dictionnaire python
        input = request.get_json()
        message = Parser(input['message'].lower())
        message.ponctuation()
        message.listIt()
        cleanMessage = message.deleteCommonWords()
        sentence = ResponsePy()

        try:
            map = Map(cleanMessage)
            coord = map.localisation()

        except IndexError:
            response = sentence.send(sentence.no)
            return jsonify({'data' : response})

        else:
            info = Wiki(coord)
            page = info.nearly()
            summary = info.about(page)
            response = sentence.send(sentence.ok)
            return jsonify({'data' : [coord, summary, response]})

    else:
        #si la method est GET
        return render_template('home.html')

# ajouter routes pour erreur 404
