from dotenv import load_dotenv
load_dotenv()


import flask
from flask import jsonify

from utils import database

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/<id>/score', methods=['GET'])
def score(id):
    return jsonify(database.get_score(id))

app.run()