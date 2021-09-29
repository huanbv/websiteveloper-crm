from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired

from src.main.modules.project.fiedls.tag_field import TagField


class TaskForm(FlaskForm):

    inputName = StringField(label='Name', validators=[
        DataRequired(message='Please fill out the name field'),
    ], render_kw={"placeholder": "Task name"})

    inputStartDate = DateTimeLocalField('Task Start Date', format='%Y-%m-%dT%H:%M',
                                        validators=[DataRequired(message="Please enter your task start date!")])

    inputDeadLine = DateTimeLocalField('Task Dead Line', format='%Y-%m-%dT%H:%M',
                                       validators=[DataRequired(message="Please enter your task dead line!")])

    inputTaskStatus = SelectField('Task Status', coerce=int)

    inputTaskPriority = SelectField('Task Priority', coerce=int)

    inputProject = SelectField('Project', coerce=int)

    tags = TagField()
