import time
import pandas as pd
import plotly
import plotly.express as px
from flask import Flask, request
from flask_cors import CORS, cross_origin

from plot_generator.generator import generate_from_user_query

app = Flask(__name__, static_folder="../build", static_url_path="/")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("index.html")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/generate_plot", methods=["POST"])
@cross_origin()
def generate():
    request_body = request.json
    user_query = request_body.get("user_query", "")
    if user_query:
        return_json = generate_from_user_query(user_query)
        return return_json
    return {"error": "No user query"}


@app.route("/register", methods=["POST"])
@cross_origin()
def register_user():
    request_body = request.json
    name = request_body.get("name", "")
    email = request_body.get("email", "")
    password = request_body.get("password", "")
    if not name or not email or not password:
        return {"success": False, "error": "Invalid Input!"}
    return {"success": True, "error": ""}


@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    request_body = request.json
    email = request_body.get("email", "")
    password = request_body.get("password", "")

    if not email or not password:
        return {"success": False, "error": "Login Failed!", "user_id": ""}
    return {"success": True, "user_id": "1", "error": ""}
