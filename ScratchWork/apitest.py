import flask
from flask import request, jsonify
import json
import requests

app = flask.Flask(__name__)

scores = {"test": "something"}

@app.route('/show', methods=['GET'])
def show():
    return json.dumps(scores)

@app.route('/update', methods=['POST'])
def update():
    global scores
    input = request.get_json()
    for name in input:
        scores[name] = input[name]
    return scores

@app.route('/add', methods=['PUT'])
def add():
    global scores
    input = request.get_json()
    for name in input:
        scores[name] = input[name]
    return scores

app.run(host='0.0.0.0', port=5000, debug=False)
