import os
from operator import itemgetter

from flask import Flask
from flask import jsonify, Response
from flask import request
from flask import make_response, render_template

from config import config
from encoder import text_encoder
from encoder import image_encoder
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

        # generating batch of image_urls and text
        batch_text = list(map(itemgetter('text'), request.json))
        batch_urls = list(map(itemgetter('image'), request.json))

        # vectorising inputs
        text_vector = text_encoder.vectorise(batch_text)
        image_vector = image_encoder.vectorise(batch_urls)

        # generating response
        for i, j, k in zip(text_vector, image_vector, request.json):
            if k['image']:
                k['image_vector'] = j
            if k['text']:
                k['text_vector'] = i

        return jsonify({"vector": request.json}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
