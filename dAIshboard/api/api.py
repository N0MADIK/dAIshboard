"""
Backend Flask API Server for dAIshboard
"""

from pathlib import Path
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

app = Flask(__name__, static_folder="../build", static_url_path="/")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(__file__).parent / 'site.db'}"

db.init_app(app)
with app.app_context():
    db.create_all()  # Create database tables


@app.errorhandler(404)
def not_found(_: object) -> object:
    """
        Gets call when a page is not found
    Args:
        _ (object): Error

    Returns:
        object: HTML page to show when other pages fail
    """
    return app.send_static_file("index.html")


@app.route("/")
def index():
    """
    First page to show when people come to the frontend
    Returns:
        object: HTML page to show when other pages fail
    """
    return app.send_static_file("index.html")


@app.route("/register", methods=["POST"])
@cross_origin()
def register_user() -> dict:
    """
        POST endpoint to allow new users to be registeted
    Returns:
        dict: Success or failure information
    """
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
def login() -> dict:
    """
        POST endpoint to allow users to login
    Returns:
        dict: Success or failure information
    """
    request_body = request.json
    email = request_body.get("email", "")
    password = request_body.get("password", "")
    user = get_user(email, password)
    if not user:
        return {"success": False, "error": "Login Failed!", "user_id": ""}
    return {"success": True, "user_id": user.id, "error": ""}


@app.route("/projects/<user_id>", methods=["GET"])
@cross_origin()
def get_projects_list(user_id: str) -> list[dict]:
    """
        GET endpoint to get list of all projects for given user
    Returns:
        list[dict]: List of projects for given user or failure information
    """
    projects = get_projects(user_id)
    return_dict = [
        {"id": p.id, "owner": p.user.name, "name": p.name, "created_on": p.created_on}
        for p in projects
    ]
    return return_dict


@app.route("/projects/<user_id>/add", methods=["POST"])
@cross_origin()
def add_new_project_to_user(user_id: str) -> dict:
    """
        POST call to add a new project to give user
    Args:
        user_id (str): User ID

    Returns:
        dict: Success or failure information
    """
    request_body = request.json
    success, error = False, ""
    try:
        success, error = add_project(user_id, request_body)
    except Exception as e:
        error = str(e)
    return {"success": success, "error": error}


@app.route("/projects/<user_id>/<project_id>/metadata", methods=["GET"])
@cross_origin()
def get_canvas_metadata(user_id: str, project_id: str) -> dict:
    """
        GET call to get the metadata for given user and project
    Args:
        user_id (str): User ID
        project_id (str): Project ID

    Returns:
        dict: Metadata for user and project
    """
    return_obj = {"data": [], "error": ""}
    return_obj["data"] = get_project_metadata(project_id, user_id)
    return return_obj


@app.route("/upload/data/<user_id>/<project_id>", methods=["POST"])
@cross_origin()
def upload_data(user_id: str, project_id: str) -> dict:
    """
        POST call to upload new data for given project and user

    Args:
        user_id (str): User ID
        project_id (str): Project ID

    Returns:
        dict: Success or failure information
    """
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
def generate(user_id: str, project_id: str) -> dict:
    """
        POST call to generate a plot
    Args:
        user_id (str): User ID
        project_id (str): Project ID

    Returns:
        dict: Plot information that is generated or Error if any
    """
    request_body = request.json
    user_query = request_body.get("user_query", "")
    if user_query:
        return_json = generate_from_user_query(user_query, user_id, project_id)
        return return_json
    return {"error": "No user query"}


@app.route("/all_plots/<user_id>/<project_id>", methods=["GET"])
@cross_origin()
def get_all_plots(user_id: str, project_id: str) -> list[dict]:
    """
        GET call to retrive all plots for a given user and project
    Args:
        user_id (str): User ID
        project_id (str): Project ID

    Returns:
        list[dict]: List of existing plots
    """
    all_plots = get_existing_plots(user_id, project_id)
    plot_jsons = [{"id": p.plot_id, "json": p.plot_json} for p in all_plots]
    return plot_jsons


@app.route("/delete_plot/<user_id>/<project_id>/<plot_id>", methods=["DELETE"])
@cross_origin()
def delete_plot(user_id: str, project_id: str, plot_id: str) -> dict:
    """
        Delete a plot from given user and project
    Args:
        user_id (str): User ID
        project_id (str): Project ID
        plot_id (str): Plot ID

    Returns:
        dict: Success or failure information
    """
    delete_plot_in_user_project(plot_id, user_id, project_id)
    return {}
