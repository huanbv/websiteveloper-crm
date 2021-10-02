from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required, current_user

from src import db
from src.main.modules.task import Task
from src.main.modules.task_checklist_item import TaskChecklistItem, TaskChecklistStatus

from src.main.modules.task_checklist_item.forms import TaskChecklistItemForm

task_checklist_item_module = Blueprint('task_checklist_item', __name__, static_folder='static',
                                       template_folder='templates')


@task_checklist_item_module.route('/', methods=['GET', 'POST'])
@login_required
def checklistItem():
    if current_user.is_authenticated:
        return render_template('task-checklist-item.html', user=current_user)
    else:
        return redirect('/')


@task_checklist_item_module.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TaskChecklistItemForm()

    # select task checklist status form task checklist status table
    form.inputTaskChecklistStatus.choices = [(p.id, p.name) for p in db.session.query(TaskChecklistStatus).all()]

    # select parent task for the task checklist item
    form.inputTask.choices = [(p.id, p.name) for p
                              in db.session.query(Task).filter_by(user_id=current_user.email).all()]

    if form.validate_on_submit():

        name = form.inputName.data
        task_checklist_status_id = form.inputTaskChecklistStatus.data
        task_id = form.inputTask.data

        task_checklist_item = TaskChecklistItem(name=name, task_checklist_status_id=task_checklist_status_id,
                                                task_id=task_id)

        # add user email to owner task checklist item
        task_checklist_item.user = current_user
        db.session.add(task_checklist_item)
        db.session.commit()
        return redirect('/task')

    return render_template('add-task-checklist-item.html', form=form, user=current_user)


@task_checklist_item_module.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    if current_user.is_authenticated:

        form = TaskChecklistItemForm()

        # re-index task checklist status form task checklist status table
        # on get request -- showing the form view
        form.inputTaskChecklistStatus.choices = [(p.id, p.name) for p in db.session.query(TaskChecklistStatus).all()]

        # re-index parent project status form project table
        form.inputTask.choices = [(p.id, p.name) for p in db.session.query(Task).filter_by(user_id=current_user
                                                                                           .email).all()]


        the_task_checklist_item = db.session.query(TaskChecklistItem).get(id)

        if form.validate_on_submit():

            the_task_checklist_item.name = form.inputName.data
            the_task_checklist_item.task_checklist_status_id = form.inputTaskChecklistStatus.data
            the_task_checklist_item.task_id = form.inputTask.data

            db.session.commit()
            return redirect('/task')

        form.inputName.default = the_task_checklist_item.name
        form.inputTaskChecklistStatus.default = the_task_checklist_item.task_checklist_status_id
        form.inputTask.default = the_task_checklist_item.task_id
        form.process()

        return render_template('/add-task-checklist-item.html', form=form, user=current_user)

    return redirect("/task-checklist-item")


@task_checklist_item_module.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    the_task_checklist_item = db.session.query(TaskChecklistItem).filter_by(id=id).first()
    db.session.delete(the_task_checklist_item)
    db.session.commit()
    return redirect(f"/task-checklist-item")


@task_checklist_item_module.route('/view/<int:id>', methods=['GET'])
@login_required
def view(id):

    if current_user.is_authenticated:

        the_task_checklist_item = db.session.query(Task).get(id)
        if not the_task_checklist_item.user == current_user:
            flash('You don\'t own this Task Checklist Item')
            return redirect('/')

        return render_template('/', task=the_task_checklist_item,  user=current_user)

    return redirect('/')
