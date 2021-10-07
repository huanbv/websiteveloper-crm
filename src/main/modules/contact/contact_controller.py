from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required, current_user

from src import db
from src.main.modules.client import Client
from src.main.modules.contact import Contact, Gender

from src.main.modules.contact.forms import ContactForm


contact_module = Blueprint('contact', __name__, static_folder='static', template_folder='templates')


@contact_module.route('/', methods=['GET', 'POST'])
@login_required
def contact():
    if current_user.is_authenticated:
        return render_template('contact.html', user=current_user)
    return redirect('/')


@contact_module.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ContactForm()

    # select contact's main client from client table
    form.inputClient.choices = [(p.id, p.name) for p in db.session.query(Client).all()]

    # select task priority form task priority table
    form.inputGender.choices = [(p.id, p.text) for p in db.session.query(Gender).all()]

    if form.validate_on_submit():

        first_name = form.inputFirstName.data
        middle_name = form.inputMiddleName.data
        last_name = form.inputLastName.data
        position = form.inputPosition.data
        email = form.inputEmail.data
        phone = form.inputPhone.data
        dob = form.inputDOB.data
        alternate_contact_number = form.inputAlternateContactNumber.data
        client_id = form.inputClient.data
        gender_id = form.inputGender.data

        the_contact = Contact(first_name=first_name, middle_name=middle_name, last_name=last_name, position=position,
                              email=email, phone=phone, dob=dob, alternate_contact_number=alternate_contact_number,
                              client_id=client_id, gender_id=gender_id)

        # add user email to owner task
        the_contact.user = current_user
        db.session.add(the_contact)
        db.session.commit()
        return redirect('/client')

    return render_template('add-contact.html', form=form, user=current_user)


@contact_module.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = ContactForm()

    # re-index company form client table
    # on get request -- showing the form view
    form.inputClient.choices = [(p.id, p.name) for p in db.session.query(Client).all()]

    # re-index contact's gender form gender table
    form.inputGender.choices = [(p.id, p.text) for p in db.session.query(Gender).all()]


    the_contact = db.session.query(Contact).get(id)

    if form.validate_on_submit():
        the_contact.first_name = form.inputFirstName.data
        the_contact.middle_name = form.inputMiddleName.data
        the_contact.last_name = form.inputLastName.data
        the_contact.position = form.inputPosition.data
        the_contact.email = form.inputEmail.data
        the_contact.phone = form.inputPhone.data
        the_contact.dob = form.inputDOB.data
        the_contact.alternate_contact_number = form.inputAlternateContactNumber.data
        the_contact.client_id = form.inputClient.data
        the_contact.gender_id = form.inputGender.data

        db.session.commit()
        return redirect('/client')

    form.inputFirstName.default = the_contact.first_name
    form.inputMiddleName.default = the_contact.middle_name
    form.inputLastName.default = the_contact.last_name
    form.inputPosition.default = the_contact.position
    form.inputEmail.default = the_contact.email
    form.inputPhone.default = the_contact.phone
    form.inputDOB.default = the_contact.dob
    form.inputAlternateContactNumber.default = the_contact.alternate_contact_number
    form.inputClient.default = the_contact.client_id
    form.inputGender.default = the_contact.gender_id

    form.process()

    return render_template('/add-contact.html', form=form, user=current_user)


@contact_module.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    the_contact = db.session.query(Contact).filter_by(id=id).first()
    db.session.delete(the_contact)
    db.session.commit()
    return redirect(f"/client")
