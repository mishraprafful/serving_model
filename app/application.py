import os

from flask import Flask
from flask import jsonify, request, Response
from flask import make_response, render_template

app = Flask(__name__, template_folder="./templates/")

# Default config vals
if os.getenv("TEST") != "True":
    os.environ["TEST"] = "False"
THEME = "default" if os.environ.get("THEME") is None else os.environ.get("THEME")
FLASK_DEBUG = (
    "True" if os.environ.get("FLASK_DEBUG") is None else os.environ.get("FLASK_DEBUG")
)

# Load config values specified above
app.config.from_object(__name__)

# Only enable Flask debugging if an env var is set to true
app.debug = app.config["FLASK_DEBUG"] in ["True", "true"]

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
