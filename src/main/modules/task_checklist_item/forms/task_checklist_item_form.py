from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class TaskChecklistItemForm(FlaskForm):

    inputName = StringField(label='Name', validators=[
        DataRequired(message='Please fill out the name field'),
    ], render_kw={"placeholder": "Task checklist item name"})

    inputTask = SelectField('Task Parent', coerce=int)

    inputTaskChecklistStatus = SelectField('Task Checklist Status', coerce=int)

