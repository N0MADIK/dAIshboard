from .models import User, db, Project, DataMetaData, PlotMetaData
from datetime import datetime

import pandas as pd
import json


def add_user(name: str, email: str, password: str):
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return True


def get_user(email: str, password: str):
    user = (
        User.query.filter(User.email == email).filter(User.password == password).first()
    )
    return user


def get_projects(user_id: str):
    projects = Project.query.filter(Project.user_id == user_id).all()
    return projects


def add_project(user_id: str, project_dict: dict):
    new_project = Project(
        name=project_dict.get("name", "MISSING"),
        created_on=datetime.now(),
        user_id=user_id,
    )
    db.session.add(new_project)
    db.session.commit()
    return True, None


def add_data_metadata(
    df: pd.DataFrame, name: str, type: str, user_id: str, project_id: str
):
    data_to_add = DataMetaData(
        name=name,
        file_type=type,
        columns=json.dumps(list(df.columns), default=str),
        types=json.dumps(df.dtypes.to_dict(), default=str),
        sample_data=df.head(5).to_json(),
        user_id=user_id,
        project_id=project_id,
    )
    db.session.add(data_to_add)
    db.session.commit()
    return True


def retrive_project_metadata(project_id: str, user_id: str):
    results = (
        DataMetaData.query.filter(DataMetaData.project_id == project_id)
        .filter(DataMetaData.user_id == user_id)
        .all()
    )
    return results


def add_plot_metadata(
    plot_id: str,
    plot_title: str,
    user_query: str,
    plot_code: str,
    plot_json: str,
    user_id: str,
    project_id: str,
):
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


def get_existing_plots(user_id: str, project_id: str):
    results = (
        PlotMetaData.query.filter(PlotMetaData.user_id == user_id)
        .filter(PlotMetaData.project_id == project_id)
        .order_by(PlotMetaData.id.desc())
        .distinct(PlotMetaData.plot_id)
    )
    results_map = [
        {"plot_id": pmd.plot_id, "plot_title": pmd.plot_title} for pmd in results
    ]
    return results_map


def get_latest_user_info_for_plot(plot_id: str, user_id: str, project_id: str):
    result = (
        PlotMetaData.query.filter(PlotMetaData.user_id == user_id)
        .filter(PlotMetaData.project_id == project_id)
        .filter(PlotMetaData.plot_id == plot_id)
        .order_by(PlotMetaData.id.desc())
        .first()
    )
    return result
