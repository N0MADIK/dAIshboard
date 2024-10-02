from flask import Flask, request
from flask_cors import CORS, cross_origin

from .plot_generator.generator import generate_from_user_query
from .utils import get_project_metadata, add_project_data
from .database import db
from .database.utils import (
    get_user,
    add_user,
    get_projects,
    add_project,
    get_existing_plots,
    delete_plot_in_user_project,
)
from pathlib import Path

app = Flask(__name__, static_folder="../build", static_url_path="/")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(__file__).parent / 'site.db'}"

db.init_app(app)
with app.app_context():
    db.create_all()  # Create database tables


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
    success, error = False, ""
    try:
        success = add_user(name, email, password)
    except Exception as e:
        error = str(e)
    return {"success": success, "error": error}


@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    request_body = request.json
    email = request_body.get("email", "")
    password = request_body.get("password", "")
    user = get_user(email, password)
    if not user:
        return {"success": False, "error": "Login Failed!", "user_id": ""}
    return {"success": True, "user_id": user.id, "error": ""}


@app.route("/projects/<user_id>", methods=["GET"])
@cross_origin()
def get_projects_list(user_id: str):
    projects = get_projects(user_id)
    return_dict = [
        {"id": p.id, "owner": p.user.name, "name": p.name, "created_on": p.created_on}
        for p in projects
    ]
    return return_dict


@app.route("/projects/<user_id>/add", methods=["POST"])
@cross_origin()
def add_new_project_to_user(user_id: str):
    request_body = request.json
    success, error = False, ""
    try:
        success, error = add_project(user_id, request_body)
    except Exception as e:
        error = str(e)
    return {"success": success, "error": error}


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
    success, error = False, ""
    try:
        if request_file:
            success = add_project_data(request_file, user_id, project_id)
    except Exception as e:
        error = str(e)
    return {"success": success, "error": error}


@app.route("/generate_plot/<user_id>/<project_id>", methods=["POST"])
@cross_origin()
def generate(user_id: str, project_id: str):
    request_body = request.json
    user_query = request_body.get("user_query", "")
    if user_query:
        return_json = generate_from_user_query(user_query, user_id, project_id)
        return return_json
    return {"error": "No user query"}


@app.route("/all_plots/<user_id>/<project_id>", methods=["GET"])
@cross_origin()
def get_all_plots(user_id: str, project_id: str):
    all_plots = get_existing_plots(user_id, project_id)
    plot_jsons = [{"id": p.plot_id, "json": p.plot_json} for p in all_plots]
    print(len(plot_jsons))
    return plot_jsons


@app.route("/delete_plot/<user_id>/<project_id>/<plot_id>", methods=["DELETE"])
@cross_origin()
def delete_plot(user_id: str, project_id: str, plot_id: str):
    delete_plot_in_user_project(plot_id, user_id, project_id)
    return {}
