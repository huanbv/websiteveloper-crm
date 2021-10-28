from flask import Blueprint, render_template, redirect, flash, session, url_for, request, make_response
from flask_login import login_required, current_user

from src import db
from src.main.modules.client import Client, ClientStatus, ClientOrder

from src.main.modules.client.forms import ClientForm, ClientStatusForm
from src.main.modules.country import Country
from src.main.modules.currency import Currency


import secrets
import pdfkit



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
                        zip_code=zip_code, client_status_id=client_status_id, country_id=country_id,
                        currency_id=currency_id)

        # add user email to owner customer
        client.user = current_user
        db.session.add(client)
        db.session.commit()
        return redirect('/client')

    form.inputClientStatus.render_kw = {'readonly': 'true', 'style': 'pointer-events: none'}
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

        return render_template('client-details.html', client=the_client, user=current_user)

    return redirect('/')


def update_shopping_cart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['colors']
    return update_shopping_cart


@client_module.route('/get-order', methods=['GET', 'POST'])
@login_required
def get_order():
    if current_user.is_authenticated:
        # client_id = current_user.email
        client_id = request.form.get('client_id')

        invoice = secrets.token_hex(5)
        update_shopping_cart
        try:
            the_order = ClientOrder(invoice=invoice, client_id=client_id,  orders=session['Shoppingcart'])

            # the_order.client_id = client_id

            db.session.add(the_order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully', 'success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('invoice.view_cart'))


@client_module.route('/order/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        orders = ClientOrder.query.filter_by(invoice=invoice).order_by(ClientOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount'] / 100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    else:
        return redirect(url_for('/'))
    return render_template('/client-order.html', invoice=invoice, tax=tax, subTotal=subTotal, grandTotal=grandTotal,
                           orders=orders, user=current_user)


@client_module.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        if request.method == "POST":
            orders = ClientOrder.query.filter_by(invoice=invoice).order_by(ClientOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = float("%.2f" % (1.06 * subTotal))

            rendered = render_template('/pdf.html', invoice=invoice, tax=tax, grandTotal=grandTotal, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] ='application/pdf'
            response.headers['content-Disposition'] ='inline; filename='+invoice+'.pdf'
            return response
    return request(url_for('orders'))
