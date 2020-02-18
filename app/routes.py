from flask import render_template, flash, request, jsonify
from app import app
from app.classes import *


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        """if method is POST, transform json into dictionnary and
        process request message from user. Return treatment result in json"""

        input = request.get_json()
        message = Parser(input["message"].lower())
        message.ponctuation()
        message.list_it()
        cleanMessage = message.delete_common_words()
        sentence = ResponsePy()

        try:
            map = Map(cleanMessage)
            coord = map.localisation()

        except IndexError:
            response = sentence.send(sentence.no)
            return jsonify({"data": response})

        else:
            info = Wiki(coord)
            page = info.nearly()
            summary = info.about(page)
            response = sentence.send(sentence.ok)
            return jsonify({"data": [coord, summary, response]})

    else:
        """if method is GET, load home page"""
        return render_template("home.html")
