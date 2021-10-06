from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required, current_user

from src import db
from src.main.modules.client import Client, ClientStatus

from src.main.modules.client.forms import ClientForm, ClientStatusForm
from src.main.modules.country import Country
from src.main.modules.currency import Currency

client_module = Blueprint('client', __name__, static_folder='static', template_folder='templates')


@client_module.route('/', methods=['GET', 'POST'])
@login_required
def client():
    if current_user.is_authenticated:
        return render_template('client.html', user=current_user)
    return redirect('/')


@client_module.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ClientForm()

    # select customer status form client status table
    form.inputClientStatus.choices = [(p.id, p.text) for p in db.session.query(ClientStatus).all()]

    # select currency unit form currency table
    form.inputCurrency.choices = [(p.id, p.name) for p in db.session.query(Currency).all()]

    # select country form country table
    form.inputCountry.choices = [(p.id, p.name) for p in db.session.query(Country).all()]

    if form.validate_on_submit():

        name = form.inputName.data
        phone = form.inputPhone.data
        email = form.inputEmail.data
        website = form.inputWebsite.data
        vat_number = form.inputVatNumber.data
        address = form.inputAddress.data
        zip_code = form.inputZIPCode.data
        client_status_id = form.inputClientStatus.data
        country_id = form.inputCountry.data
        currency_id = form.inputCurrency.data

        client = Client(name=name, phone=phone, email=email, website=website, vat_number=vat_number, address=address,
                        zip_code=zip_code, client_status_id=client_status_id, country_id=country_id, currency_id=currency_id)

        # add user email to owner customer
        client.user = current_user
        db.session.add(client)
        db.session.commit()
        return redirect('/client')

    return render_template('add-client.html', form=form, user=current_user)


@client_module.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = ClientForm()

    # re-index customer status form client status table
    # on get request -- showing the form view
    form.inputClientStatus.choices = [(p.id, p.text) for p in db.session.query(ClientStatus).all()]

    # re-index currency unit form currency table
    form.inputCurrency.choices = [(p.id, p.name) for p in db.session.query(Currency).all()]

    # re-index country form country table
    form.inputCountry.choices = [(p.id, p.name) for p in db.session.query(Country).all()]

    the_client = db.session.query(Client).get(id)

    if form.validate_on_submit():

        the_client.name = form.inputName.data
        the_client.phone = form.inputPhone.data
        the_client.email = form.inputEmail.data
        the_client.website = form.inputWebsite.data
        the_client.vat_number = form.inputVatNumber.data
        the_client.address = form.inputAddress.data
        the_client.zip_code = form.inputZIPCode.data
        the_client.client_status_id = form.inputClientStatus.data
        the_client.country_id = form.inputCountry.data
        the_client.currency_id = form.inputCurrency.data

        db.session.commit()
        return redirect('/client')

    form.inputName.default = the_client.name
    form.inputPhone.default = the_client.phone
    form.inputEmail.default = the_client.email
    form.inputWebsite.default = the_client.website
    form.inputVatNumber.default = the_client.vat_number
    form.inputAddress.default = the_client.address
    form.inputZIPCode.default = the_client.zip_code
    form.inputClientStatus.default = the_client.client_status_id
    form.inputCountry.default = the_client.country_id
    form.inputCurrency.default = the_client.currency_id

    form.process()

    return render_template('/add-client.html', form=form, user=current_user)


@client_module.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    the_client = db.session.query(Client).filter_by(id=id).first()
    db.session.delete(the_client)
    db.session.commit()
    return redirect(f"/client")


@client_module.route('/view/<int:id>', methods=['GET'])
@login_required
def view(id):

    if current_user.is_authenticated:

        the_client = db.session.query(Client).get(id)
        if not the_client.user == current_user:
            flash('You don\'t have any customer information')
            return redirect('/')

        return render_template('client-details.html', client=the_client,  user=current_user)

    return redirect('/')
