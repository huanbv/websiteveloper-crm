from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired

from src.main.modules.project.fiedls.tag_field import TagField


class ProjectForm(FlaskForm):

    inputName = StringField(label='Name', validators=[
        DataRequired(message='Please fill out the name field'),
    ], render_kw={"placeholder": "Project name"})

    inputStartDate = DateTimeLocalField('Project Start Date', format='%Y-%m-%dT%H:%M',
                                        validators=[DataRequired(message="Please enter your project start date!")])

    inputDeadLine = DateTimeLocalField('Project Dead Line', format='%Y-%m-%dT%H:%M',
                                       validators=[DataRequired(message="Please enter your project dead line!")])

    inputProjectStatus = SelectField('Project Status', coerce=int)

    tags = TagField()
