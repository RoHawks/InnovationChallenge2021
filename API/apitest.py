import flask
from flask import request, jsonify, Response
import json
import requests

app = flask.Flask(__name__)

scores = {"test": "something"}

@app.route("/background.js")
def js():
    with open('docs/background.js', 'r') as f:
        js = f.read()
        return js

@app.route("/style.css")
def css():
    with open('docs/style.css', 'r') as f:
        css = f.read()
        return Response(css, mimetype="text/css")

@app.route("/assets/logo.png")
def logo():
    with open('docs/assets/logo.png', 'rb') as f:
        logo = f.read()
        return Response(logo, mimetype="image/png")

# Annotation that allows the function to be hit at the specific URL.
@app.route("/")
# Generic Python functino that returns "Hello world!"
def index():
    with open('docs/index.html', 'r') as f:
        html = f.read()
        return html

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
