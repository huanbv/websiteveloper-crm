from sqlalchemy import ForeignKey, Sequence, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from src import db


class Task(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, Sequence('task_id_seg'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    dead_line = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('user.email'))
    user = relationship('User', backref='tasks')

    task_status_id = db.Column(db.Integer, ForeignKey('task_status.id'))
    task_status = relationship('TaskStatus', backref='tasks')

    task_priority_id = db.Column(db.Integer, ForeignKey('task_priority.id'))
    task_priority = relationship('TaskPriority', backref='tasks')

    project_id = db.Column(db.Integer, ForeignKey('project.id'))
    project = relationship('Project', backref='tasks')


    def __init__(self, name: str, start_date: str, dead_line: str, task_status_id: str, task_priority_id: str,
                 project_id: str):
        """
        The constructor for Task model.
        :param name: The task's name
        :param start_date: The task's start date
        :param dead_line: The dead line of the task
        :param task_status_id: The task status of the task
        :param task_priority_id: The task priority of the task
        :param project_id: The parent project of the task
        """
        self.name = name
        self.start_date = start_date
        self.dead_line = dead_line
        self.task_status_id = task_status_id
        self.task_priority_id = task_priority_id
        self.project_id = project_id


    def get_status_class(self):
        if self.task_status_id == 1:
            return "border border-gray-500 text-gray-700"
        elif self.task_status_id == 2:
            return "border border-blue-500 text-blue-700"
        elif self.task_status_id == 3:
            return "border border-yellow-500 text-yellow-700"
        elif self.task_status_id == 4:
            return "border border-pink-500 text-pink-700"
        else:
            return "border border-green-500 text-green-700"

    def get_priority_class(self):
        if self.task_priority_id == 1:
            return "border border-black-500 text-black-700"
        elif self.task_priority_id == 2:
            return "border border-blue-500 text-blue-700"
        else:
            return "border border-red-500 text-red-700"


class TaskStatus(db.Model):
    id = db.Column(db.Integer, Sequence('task_status_id_seq'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Task Status: {} with {}>'.format(self.id, self.name)


class TaskPriority(db.Model):
    id = db.Column(db.Integer, Sequence('task_priority_id_seq'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Task Priority: {} with {}>'.format(self.id, self.name)


class TaskTag(db.Model):
    task_id = db.Column(db.Integer, ForeignKey('task.id'))
    task = relationship('Task', backref=db.backref('task_tags',
                                        cascade="save-update, merge, "
                                                "delete, delete-orphan"))

    tag_id = db.Column(db.Integer, ForeignKey('tag.id'))
    tag = relationship('Tag', backref=db.backref('task_tags',
                                        cascade="save-update, merge, "
                                                "delete, delete-orphan"))

    __table_args__ = (
        PrimaryKeyConstraint(task_id, tag_id),
    )
