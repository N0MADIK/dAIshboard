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


class DataMetaData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(150), nullable=False)
    columns = db.Column(db.JSON, nullable=False)
    types = db.Column(db.JSON, nullable=False)
    sample_data = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id), nullable=False)

    user = db.relationship("User", foreign_keys="DataMetaData.user_id")
    project = db.relationship("Project", foreign_keys="DataMetaData.project_id")

    def __repr__(self):
        return f"Data MetaData {self.name} ({self.file_type})"


class PlotMetaData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plot_id = db.Column(db.String(150), nullable=False)
    plot_title = db.Column(db.String(150), nullable=False)
    user_query = db.Column(db.TEXT, nullable=False)
    plot_code = db.Column(db.TEXT, nullable=False)
    plot_json = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id), nullable=False)

    user = db.relationship("User", foreign_keys="PlotMetaData.user_id")
    project = db.relationship("Project", foreign_keys="PlotMetaData.project_id")

    def __repr__(self):
        return f"Plot MetaData {self.plot_id} {self.plot_title}"
