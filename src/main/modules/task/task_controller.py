from flask import Blueprint, render_template, redirect, flash, request
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
def task():
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
    form.inputTaskStatus.render_kw = {'readonly': 'true', 'style': 'pointer-events: none'}
    return render_template('add-task.html', form=form, user=current_user, tags=tags)


@task_module.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.is_authenticated:

        form = TaskForm()

        # gan cac tags da chon
        from src.main.modules.task.task_model import TaskTag
        form.tags.default = [tag.tag_id for tag in TaskTag.query.filter_by(task_id=id).all()]

        # re-index task status form task status table
        # on get request -- showing the form view
        form.inputTaskStatus.choices = [(p.id, p.name) for p in db.session.query(TaskStatus).all()]

        # re-index parent project status form project table
        form.inputProject.choices = [(p.id, p.name) for p in db.session.query(Project).filter_by(user_id=current_user
                                                                                                 .email).all()]


        # re-index task priority
        form.inputTaskPriority.choices = [(p.id, p.name) for p in db.session.query(TaskPriority).all()]

        the_task = db.session.query(Task).get(id)

        if form.validate_on_submit():
            print(form.tags.data)
            print(the_task.task_tags)

            the_task.name = form.inputName.data
            the_task.start_date = form.inputStartDate.data
            the_task.dead_line = form.inputDeadLine.data
            the_task.task_status_id = form.inputTaskStatus.data
            the_task.project_id = form.inputProject.data
            the_task.task_priority_id = form.inputTaskPriority.data
            the_task.task_tags = [TaskTag(task_id=the_task.id, tag_id=tag_id) for tag_id in form.tags.data]

            db.session.commit()
            return redirect('/task')
            # invoking this to update the associated project status
            update_project_status(the_task.project)
            return redirect(f"/project")
            # return redirect(f"/project/{request.args.get('project_id')}")


        form.inputName.default = the_task.name
        form.inputStartDate.default = the_task.start_date
        form.inputDeadLine.default = the_task.dead_line
        form.inputTaskStatus.default = the_task.task_status_id
        form.inputProject.default = the_task.project_id
        form.inputTaskPriority.default = the_task.task_priority_id
        form.process()

        tags = Tag.query.all()
        return render_template('/add-task.html', form=form, user=current_user, tags=tags)

    return redirect("/")


def update_project_status(the_project):
    in_progress_tasks = list(filter(lambda task: task.task_status_id == 2, the_project.tasks))
    # at least 1 in progress task is exists
    if len(in_progress_tasks) >= 1:
        the_project.project_status_id = 2
        db.session.commit()
        return

    finished_tasks = list(filter(lambda task: task.task_status_id == 2, the_project.tasks))
    # all the tasks in the_project have completed
    if len(finished_tasks) == len(the_project.tasks):
        the_project.project_status_id = 5
        db.session.commit()
        return

    # otherwise, it's not started
    the_project.project_status_id = 1
    db.session.commit()


@task_module.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    the_task = db.session.query(Task).filter_by(id=id).first()
    db.session.delete(the_task)
    db.session.commit()
    return redirect(f"/task")


@task_module.route('/view/<int:id>', methods=['GET'])
@login_required
def view(id):

    if current_user.is_authenticated:

        the_task = db.session.query(Task).get(id)
        if not the_task.user == current_user:
            flash('You don\'t own this Task Checklist Item')
            return redirect('/')

        return render_template('/task-details.html', task=the_task,  user=current_user)

    return redirect('/')
