"""
Contains functions to interact with the database
"""

import json
from datetime import datetime
import pandas as pd

from .models import User, db, Project, DataMetaData, PlotMetaData


def add_user(name: str, email: str, password: str) -> bool:
    """
        Add a user to the database
    Args:
        name (str): User name
        email (str): User email
        password (str): User password

    Returns:
        bool: True if successful
    """
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return True


def get_user(email: str, password: str) -> User:
    """
        Get a user using email and password
    Args:
        email (str): User email
        password (str): User password
    Returns:
        User: User object for the given user. None if user doesnt exist
    """
    user = (
        User.query.filter(User.email == email).filter(User.password == password).first()
    )
    return user


def get_projects(user_id: str) -> list[Project]:
    """
        Get list of projects for given user

    Args:
        user_id (str): User ID

    Returns:
        list[Project]: List of Projects for given user
    """
    projects = Project.query.filter(Project.user_id == user_id).all()
    return projects


def add_project(user_id: str, project_dict: dict) -> tuple[bool, object]:
    """
        Add a new project to given user
    Args:
        user_id (str): User ID
        project_dict (dict): Project Information as a dictionary

    Returns:
        tuple[bool, Project]: True,None if successful
    """
    new_project = Project(
        name=project_dict.get("name", "MISSING"),
        created_on=datetime.now(),
        user_id=user_id,
    )
    db.session.add(new_project)
    db.session.commit()
    return True, None


def add_data_metadata(
    df: pd.DataFrame, name: str, file_type: str, user_id: str, project_id: str
) -> bool:
    """
        Add metadata for given dataset to the database
    Args:
        df (pd.DataFrame): DataFrame containing the data
        name (str): Name of the dataset
        file_type (str): Type of the dataset
        user_id (str): User ID
        project_id (str): Project ID

    Returns:
        bool: True if successful
    """
    data_to_add = DataMetaData(
        name=name,
        file_type=file_type,
        columns=json.dumps(list(df.columns), default=str),
        types=json.dumps(df.dtypes.to_dict(), default=str),
        sample_data=df.head(5).to_json(),
        user_id=user_id,
        project_id=project_id,
    )
    db.session.add(data_to_add)
    db.session.commit()
    return True


def retrive_project_metadata(project_id: str, user_id: str) -> list[DataMetaData]:
    """
        Get the project metadata for a given project and user
    Args:
        project_id (str): Project ID
        user_id (str): User ID

    Returns:
        list[DataMetaData]: List of metadata for the data in the project of the given user
    """
    results = (
        DataMetaData.query.filter(DataMetaData.project_id == project_id)
        .filter(DataMetaData.user_id == user_id)
        .all()
    )
    return results


def add_plot_metadata(*args: list[str]) -> bool:
    """
        Add plot metadata to the plot
    Returns:
        bool: True if successful
    """
    plot_id, plot_title, user_query, plot_code, plot_json, user_id, project_id = args
    plot_data_to_add = PlotMetaData(
        plot_id=plot_id,
        plot_title=plot_title,
        user_query=user_query,
        plot_code=plot_code,
        plot_json=plot_json,
        user_id=user_id,
        project_id=project_id,
    )
    db.session.add(plot_data_to_add)
    db.session.commit()
    return True


def get_existing_plots(user_id: str, project_id: str) -> list[object]:
    """
        Get the existing plots in a given project for a given user
    Args:
        user_id (str): User ID
        project_id (str): Project ID

    Returns:
        list[object]: List of plots
    """
    results = (
        PlotMetaData.query.filter(PlotMetaData.user_id == user_id)
        .filter(PlotMetaData.project_id == project_id)
        .order_by(PlotMetaData.id.desc())
        .distinct(PlotMetaData.plot_id)
    )
    ids, return_list = set(), []
    for p in results:
        if p.plot_id not in ids:
            ids.add(p.plot_id)
            return_list.append(p)
    return return_list


def get_latest_user_info_for_plot(
    plot_id: str, user_id: str, project_id: str
) -> list[PlotMetaData]:
    """
        Get the latest user info for a given plot
    Args:
        plot_id (str): Plot ID
        user_id (str): User ID
        project_id (str): Project ID

    Returns:
        list[PlotMetaData]: List of plot metadata
    """
    result = (
        PlotMetaData.query.filter(PlotMetaData.user_id == user_id)
        .filter(PlotMetaData.project_id == project_id)
        .filter(PlotMetaData.plot_id == plot_id)
        .order_by(PlotMetaData.id.desc())
        .first()
    )
    return result


def delete_plot_in_user_project(plot_id: str, user_id: str, project_id: str) -> bool:
    """
        Delete a plot in given project for given user
    Args:
        plot_id (str): Plot ID
        user_id (str): User ID
        project_id (str): Project ID

    Returns:
        bool: True if succesful
    """
    db.session.query(PlotMetaData).filter(PlotMetaData.user_id == user_id).filter(
        PlotMetaData.project_id == project_id
    ).filter(PlotMetaData.plot_id == plot_id).delete()
    db.session.commit()
    return True
