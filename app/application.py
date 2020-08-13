import os

from flask import Flask
from flask import jsonify, request, Response
from flask import make_response, render_template

from config import config

app = Flask(__name__, template_folder="./templates/")

# Load config values from config
app.config.from_object(config)

# html rendered homepage
@app.route("/", methods=["GET"])
def index():
    headers = {"Content-Type": "text/html"}
    return make_response(render_template("index.html"), 200, headers)


# vectoriser endpoint
@app.route("/vectorise", methods=["POST"])
def vectoriser():
    vector = [1, 2, 3]
    return jsonify({"vector": vector}), 200, {"content-type": "application/json"}


if __name__ == "__main__":
    app.run()
