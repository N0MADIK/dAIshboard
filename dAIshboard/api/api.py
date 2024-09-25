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


@app.route("/api/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/generate_plot", methods=["POST"])
@cross_origin()
def generate():
    request_body = request.json
    user_query = request_body.get("user_query", "")
    if user_query:
        print("User Query Found!!", user_query, flush=True)
        return_json = generate_from_user_query(user_query)
        print("Return Json is!!", return_json, flush=True)
        return return_json
    return {"error": "No user query"}


@app.route("/plot")
@cross_origin()
def plot_test():
    df = pd.DataFrame(
        {
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
        }
    )
    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="stack", title="Test")
    fig.update_layout(title_x=0.5)
    graphJSON = plotly.io.to_json(fig, pretty=True)
    return graphJSON
