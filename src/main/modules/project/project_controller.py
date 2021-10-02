from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required, current_user

from src import db
from src.main.modules.project import Project, ProjectStatus

from src.main.modules.project.forms import ProjectForm
from src.main.modules.project.project_model import ProjectTag
from src.main.modules.tag.tag_model import Tag

project_module = Blueprint('project', __name__, static_folder='static', template_folder='templates')


@project_module.route('/', methods=['GET', 'POST'])
@login_required
def project():
    if current_user.is_authenticated:
        return render_template('project.html', user=current_user)
    else:
        return redirect('/')


@project_module.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ProjectForm()

    # select project status form project status table
    form.inputProjectStatus.choices = [(p.id, p.text) for p in db.session.query(ProjectStatus).all()]

    if form.validate_on_submit():
        print(form.tags.data)

        name = form.inputName.data
        dead_line = form.inputDeadLine.data
        start_date = form.inputStartDate.data
        project_status_id = form.inputProjectStatus.data

        project = Project(name=name, start_date=start_date, dead_line=dead_line, project_status_id=project_status_id)
        project.project_tags = [ProjectTag(project_id=project.id, tag_id=tag_id) for tag_id in form.tags.data]

        # add user email to owner project
        project.user = current_user
        db.session.add(project)
        db.session.commit()
        return redirect('/project')

    tags = Tag.query.all()
    return render_template('add-project.html', form=form, user=current_user, tags=tags)


@project_module.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    form = ProjectForm()

    # gan cac tags da chon
    from src.main.modules.project.project_model import ProjectTag
    form.tags.default = [tag.tag_id for tag in ProjectTag.query.filter_by(project_id=id).all()]

    # re-index project status form project status table
    # on get request -- showing the form view
    form.inputProjectStatus.choices = [(p.id, p.text) for p in db.session.query(ProjectStatus).all()]

    the_project = db.session.query(Project).get(id)

    if form.validate_on_submit():
        print(form.tags.data)
        print(the_project.project_tags)

        the_project.name = form.inputName.data
        the_project.start_date = form.inputStartDate.data
        the_project.dead_line = form.inputDeadLine.data
        the_project.project_status_id = form.inputProjectStatus.data
        the_project.project_tags = [ProjectTag(project_id=the_project.id, tag_id=tag_id) for tag_id in form.tags.data]

        db.session.commit()
        return redirect('/project')

    form.inputName.default = the_project.name
    form.inputStartDate.default = the_project.start_date
    form.inputDeadLine.default = the_project.dead_line
    form.inputProjectStatus.default = the_project.project_status_id
    form.process()

    tags = Tag.query.all()
    return render_template('/add-project.html', form=form, user=current_user, tags=tags)


@project_module.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    the_project = db.session.query(Project).filter_by(id=id).first()
    db.session.delete(the_project)
    db.session.commit()
    return redirect(f"/project")


@project_module.route('/view/<int:id>', methods=['GET'])
@login_required
def view(id):

    if current_user.is_authenticated:

        the_project = db.session.query(Project).get(id)
        if not the_project.user == current_user:
            flash('You don\'t own this Project')
            return redirect('/')

        return render_template('view.html', project=the_project,  user=current_user)

    return redirect('/')
