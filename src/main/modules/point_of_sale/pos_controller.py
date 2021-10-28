import secrets

from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from flask_login import login_required, current_user

from src import db
from src.main.modules.client import Client

from src.main.modules.currency import Currency
from src.main.modules.invoice import PaymentStatus, DeliveryStatus, Invoice
from src.main.modules.invoice.invoice_model import InvoiceItem


from src.main.modules.invoice.forms import InvoiceForm
from src.main.modules.product import Product

pos_module = Blueprint('pos', __name__, static_folder='static', template_folder='templates')


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@pos_module.route('/', methods=['GET', 'POST'])
@login_required
def view_cart():
    if current_user.is_authenticated:
        products = Product.query.all()
        clients = Client.query.all()
        if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
            return render_template('pos.html', user=current_user, products=products, clients=clients)
        subtotal = 0
        grandtotal = 0
        for key, product in session['Shoppingcart'].items():
            discount = (product['discount'] / 100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            tax = ("%.2f" % (.06 * float(subtotal)))
            grandtotal = float("%.2f" % (1.06 * subtotal))

        return render_template('pos.html', user=current_user, tax=tax, grandtotal=grandtotal, products=products
                               ,clients=clients)
    # return redirect('/')
    return render_template('pos.html', user=current_user)



@pos_module.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')
        product = Product.query.filter_by(id=product_id).first()

        if request.method == "POST":
            dictItems = {product_id: {
                'name': product.name,
                'price': float(product.price),
                'discount': product.discount,
                'color': color,
                'quantity': quantity,
                'colors': product.colors}}

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], dictItems)
                    return redirect(request.referrer)

            else:
                session['Shoppingcart'] = dictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@pos_module.route('/update/<int:code>', methods=['POST'])
def update_cart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('pos.view_cart'))
        # return redirect(url_for('/'))
    if request.method == "POST":
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated!')
                    return redirect(url_for('pos.viewCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('pos.view_cart'))


@pos_module.route('/delete-item/<int:id>')
def delete_item(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        # return redirect(url_for('/'))
        return redirect(url_for('pos.view_cart'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('pos.view_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('pos.view_cart'))


@pos_module.route('/clear-cart')
def clear_cart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('/'))
    except Exception as e:
        print(e)
        return redirect(url_for('pos.view_cart'))


# @pos_module.route('/add', methods=['GET', 'POST'])
# @login_required
# def add():
#     form = InvoiceForm()
#
#     # select payment status form payment status table
#     form.inputPaymentStatus.choices = [(p.id, p.text) for p in db.session.query(PaymentStatus).all()]
#
#     # select Delivery status form Delivery status table
#     form.inputDeliveryStatus.choices = [(p.id, p.text) for p in db.session.query(DeliveryStatus).all()]
#
#     # select client form client table
#     form.inputClient.choices = [(p.id, p.name) for p in db.session.query(Client).all()]
#
#     # select currency form currency table
#     form.inputCurrency.choices = [(p.id, p.name) for p in db.session.query(Currency).all()]
#
#     invoice_hex = 'INV-' + secrets.token_hex(2)
#
#     if form.validate_on_submit():
#         print(form.items.data)
#
#         client_id = form.inputClient.data
#         payment_status_id = form.inputPaymentStatus.data
#         delivery_status_id = form.inputDeliveryStatus.data
#         currency_id = form.inputCurrency.data
#
#         invoice = Invoice(invoice=invoice_hex, client_id=client_id, payment_status_id=payment_status_id,
#                               currency_id=currency_id, delivery_status_id=delivery_status_id)
#         invoice.invoice_items = [InvoiceItem(invoice_id=invoice.id, product_id=product_id) for product_id in
#                                      form.items.data]
#
#         # add user email to owner invoice
#         db.session.add(invoice)
#         db.session.commit()
#         return redirect('/invoice')
#
#     form.inputPaymentStatus.render_kw = {'readonly': 'true', 'style': 'pointer-events: none'}
#     form.inputDeliveryStatus.render_kw = {'readonly': 'true', 'style': 'pointer-events: none'}
#
#     items = Product.query.all()
#
#     return render_template('add-invoice.html', form=form, user=current_user, items=items)
