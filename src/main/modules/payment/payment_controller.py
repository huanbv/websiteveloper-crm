from flask import Blueprint, redirect, request, url_for
from flask_login import login_required

from src import db
from src.main.modules.client import ClientOrder, Client, ClientOrderHistory

payment_module = Blueprint('payment', __name__, static_folder='static', template_folder='templates')


@payment_module.route('/confirm', methods=['POST'])
@login_required
def payment():
    invoice = request.form.get('invoice')
    client_id = request.form.get('client_id')
    client = Client.query.filter_by(id=client_id).first()

    orders = ClientOrder.query.filter_by(client_id=client_id,
                                           invoice=invoice).order_by(ClientOrder.id.desc()).first()

    for _key, product in orders.orders.items():
        order = ClientOrderHistory(invoice=invoice, status="Paid", client_id=client_id,
                             client_name=client.name, country=client.country, city=client.city,
                             contact=client.contact, zipcode=client.zip_code,
                             product_id=int(_key), product_name=product['name'],
                             product_price=product['price'], product_quantity=product['quantity'],
                             product_detail=product['color'])

        db.session.add(order)
        # print('Your order has been sent successfully','success')

    orders.status = "Paid"
    db.session.commit()
    return redirect(url_for('pos.view_cart'))

