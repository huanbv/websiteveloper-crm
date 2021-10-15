from sqlalchemy import ForeignKey, Sequence, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from src import db


class Project(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, Sequence('project_id_seg'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    dead_line = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('user.email'))
    user = relationship('User', backref='projects')

    project_status_id = db.Column(db.Integer, ForeignKey('project_status.id'))
    project_status = relationship('ProjectStatus', backref='projects')

    client_id = db.Column(db.Integer, ForeignKey('client.id'))
    client = relationship('Client', backref='projects')

    def __init__(self, name: str, start_date: str, dead_line: str, project_status_id: str, client_id: str):
        """
        The constructor for Project model.
        :param name: The project's name
        :param start_date: The project's start date
        :param dead_line: The dead line of the project
        """
        self.name = name
        self.start_date = start_date
        self.dead_line = dead_line
        self.project_status_id = project_status_id
        self.client_id = client_id

    def get_status_class(self):
        if self.project_status_id == 1:
            return "border border-gray-500 text-gray-700"
        elif self.project_status_id == 2:
            return "border border-blue-500 text-blue-700"
        elif self.project_status_id == 3:
            return "border border-yellow-500 text-yellow-700"
        elif self.project_status_id == 4:
            return "border border-pink-500 text-pink-700"
        else:
            return "border border-green-500 text-green-700"


class ProjectStatus(db.Model):
    id = db.Column(db.Integer, Sequence('project_status_id_seq'), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Project Status: {} with {}>'.format(self.id, self.text)


class ProjectTag(db.Model):
    project_id = db.Column(db.Integer, ForeignKey('project.id'))
    project = relationship('Project', backref=db.backref('project_tags',
                                        cascade="save-update, merge, "
                                                "delete, delete-orphan"))

    tag_id = db.Column(db.Integer, ForeignKey('tag.id'))
    tag = relationship('Tag', backref=db.backref('project_tags',
                                        cascade="save-update, merge, "
                                                "delete, delete-orphan"))

    __table_args__ = (
        PrimaryKeyConstraint(project_id, tag_id),
    )
