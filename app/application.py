import os

from flask import Flask
from flask import jsonify, Response
from flask import request
from flask import make_response, render_template

from config import config
from utils.request_parser import parse_request

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
def vectorise():

    auth = request.headers.get("Content-Type")

    # verifying headers
    if auth != 'application/json':
        return jsonify({"Status": "Unauthorised Access"}), 401

    # parsing reequest
    error, req = parse_request(request)
    if error is not None:
        return jsonify(error), 402
    else:
        vector = [1, 2, 3]
        return jsonify({"vector": vector}), 200


if __name__ == "__main__":
    app.run()
