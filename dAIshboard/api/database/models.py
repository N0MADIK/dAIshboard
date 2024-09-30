from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    user = db.relationship("User", foreign_keys="Project.user_id")

    def __repr__(self):
        return f"Project ('{self.name}', '{self.user.name}', '{self.created_on}', '{self.user_id}')"
