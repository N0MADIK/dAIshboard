from flask import Flask, request
from flask_cors import CORS, cross_origin

from .plot_generator.generator import generate_from_user_query
from .utils import get_project_metadata

app = Flask(__name__, static_folder="../build", static_url_path="/")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("index.html")


@app.route("/")
def index():
    return app.send_static_file("index.html")


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


@app.route("/projects/<user_id>", methods=["GET"])
@cross_origin()
def get_projects_list(user_id: str):
    projects = [
        {
            "id": "728ed52f",
            "name": "Test",
            "owner": "Tester",
            "created_on": "09-18-2024",
        }
    ]
    return projects


@app.route("/projects/<user_id>/add", methods=["POST"])
@cross_origin()
def add_new_project_to_user(user_id: str):
    request_body = request.json
    return {"success": True, "error": ""}


@app.route("/projects/<user_id>/<project_id>/metadata", methods=["GET"])
@cross_origin()
def get_canvas_metadata(user_id: str, project_id: str):
    return_obj = {"data": [], "error": ""}
    return_obj["data"] = get_project_metadata(project_id, user_id)
    return return_obj


@app.route("/upload/data/<user_id>/<project_id>", methods=["POST"])
@cross_origin()
def upload_data(user_id: str, project_id: str):
    request_file = request.files.get("file")
    return {"success": True, "error": ""}


@app.route("/generate_plot/<user_id>/<project_id>", methods=["POST"])
@cross_origin()
def generate(user_id: str, project_id: str):
    request_body = request.json
    user_query = request_body.get("user_query", "")
    if user_query:
        return_json = generate_from_user_query(user_query)
        return return_json
    return {"error": "No user query"}
