from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src import db
from src.main.modules.project import Project
from src.main.modules.task import Task, TaskStatus, TaskPriority

from src.main.modules.task.forms import TaskForm
from src.main.modules.task.task_model import TaskTag
from src.main.modules.tag.tag_model import Tag

task_module = Blueprint('task', __name__, static_folder='static', template_folder='templates')


@task_module.route('/', methods=['GET', 'POST'])
@login_required
def project():
    if current_user.is_authenticated:
        return render_template('task.html', user=current_user)
    return redirect('/')


@task_module.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TaskForm()

    # select task status form task status table
    form.inputTaskStatus.choices = [(p.id, p.name) for p in db.session.query(TaskStatus).all()]

    # select task priority form task priority table
    form.inputTaskPriority.choices = [(p.id, p.name) for p in db.session.query(TaskPriority).all()]

    # select parent project for the task
    form.inputProject.choices = [(p.id, p.name) for p in
                                 db.session.query(Project).filter_by(user_id=current_user.email).all()]

    if form.validate_on_submit():
        print(form.tags.data)

        name = form.inputName.data
        dead_line = form.inputDeadLine.data
        start_date = form.inputStartDate.data
        task_status_id = form.inputTaskStatus.data
        task_priority_id = form.inputTaskPriority.data
        project_id = form.inputProject.data

        task = Task(name=name, start_date=start_date, dead_line=dead_line, task_status_id=task_status_id,
                    task_priority_id=task_priority_id, project_id=project_id)
        task.task_tags = [TaskTag(task_id=task.id, tag_id=tag_id) for tag_id in form.tags.data]

        # add user email to owner task
        task.user = current_user
        db.session.add(task)
        db.session.commit()
        return redirect('/task')

    tags = Tag.query.all()
    return render_template('add-task.html', form=form, user=current_user, tags=tags)
