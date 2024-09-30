from .models import User, db


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
