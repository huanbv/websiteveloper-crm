from sqlalchemy import ForeignKey, Sequence
from sqlalchemy.orm import relationship

from src import db


class TaskChecklistItem(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, Sequence('task_checklist_item_id_seg'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('user.email'))
    user = relationship('User', backref='task_checklist_items')

    task_checklist_status_id = db.Column(db.Integer, ForeignKey('task_checklist_status.id'))
    task_status = relationship('TaskChecklistStatus', backref='task_checklist_items')

    task_id = db.Column(db.Integer, ForeignKey('task.id'))
    task = relationship('Task', backref='task_checklist_items')


    def __init__(self, name: str, task_checklist_status_id: str, task_id: str):
        """
        The constructor for Task model.
        :param name: The task checklist item's name
        :param task_checklist_status_id: The task checklist status
        :param task_id: The parent task of the task checklist item
        """
        self.name = name
        self.task_checklist_status_id = task_checklist_status_id
        self.task_id = task_id


class TaskChecklistStatus(db.Model):
    id = db.Column(db.Integer, Sequence('task_checklist_status_id_seq'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Task Checklist Status: {} with {}>'.format(self.id, self.name)

