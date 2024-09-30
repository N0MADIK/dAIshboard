from .models import User, db, Project
from datetime import datetime


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
