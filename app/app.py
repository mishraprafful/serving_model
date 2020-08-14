from app.utils.request_parser import parse_request
from app.encoder.image_encoder import ImageEncoder
from app.encoder.text_encoder import TextEncoder
from app.config import config
import os
import sys
from operator import itemgetter

from flask import Flask
from flask import jsonify, Response
from flask import request
from flask import make_response, render_template

import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


# init ecnoders
text_model = TextEncoder()
image_model = ImageEncoder()
logger.info("Models Imported Sucessfully")

app = Flask(__name__, template_folder="./templates/")

# Load config values from config
app.config.from_object(config)
logger.info("Config Imported Successfully")

# html rendered homepage


@app.route("/", methods=["GET"])
def index():
    headers = {"Content-Type": "text/html"}
    logger.info("Rendered HTML Page")
    return make_response(render_template("index.html"), 200, headers)


# vectoriser endpoint
@app.route("/vectorise", methods=["POST"])
def vectorise():

    auth = request.headers.get("Content-Type")

    # verifying headers
    if auth != 'application/json':
        logger.error("Not Authorised")
        return jsonify({"Status": "Unauthorised Access"}), 401

    logger.info("Autorization Successful")

    # parsing reequest
    error, req = parse_request(request)
    if error is not None:
        logger.error("Invalid Request! Parsing Unsucessful")
        return jsonify(error), 402
    else:

        logger.info("Request Parsed")

        # generating batch of image_urls and text
        batch_text = list(map(itemgetter('text'), request.json))
        batch_urls = list(map(itemgetter('image'), request.json))

        logger.info("Batches generated")

        # vectorising inputs
        text_vector = text_model.vectorise(batch_text)
        image_vector = image_model.vectorise(batch_urls)

        logger.info("Vectorisation Successful")

        # generating response
        for i, j, k in zip(text_vector, image_vector, request.json):
            if k['image']:
                k['image_vector'] = j
            if k['text']:
                k['text_vector'] = i

        logger.info("Formed Response Successfully")

        return jsonify(request.json), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
