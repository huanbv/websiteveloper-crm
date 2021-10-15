import secrets

from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from flask_login import login_required, current_user

from src import db
from src.main.modules.client import Client, ClientStatus, ClientOrder
from src.main.modules.client.client_controller import orders, client_module

from src.main.modules.client.forms import ClientForm, ClientStatusForm
from src.main.modules.country import Country
from src.main.modules.currency import Currency
from src.main.modules.product import Product

invoice_module = Blueprint('invoice', __name__, static_folder='static', template_folder='templates')


@invoice_module.route('/', methods=['GET', 'POST'])
@login_required
def invoice():
    if current_user.is_authenticated:
        the_client_order = ClientOrder.query.all()
        return render_template('invoice.html', user=current_user, ClientOrder=the_client_order)
    return redirect('/')

#
# @invoice_module.route('/')
# def index():
#     try:
#         the_client_order = ClientOrder.query.filter_by(style='mini').order_by(Sock.name).all()
#         sock_text = '<ul>'
#         for sock in socks:
#             sock_text += '<li>' + sock.name + ', ' + sock.color + '</li>'
#         sock_text += '</ul>'
#         return sock_text
#     except Exception as e:
#         # e holds description of the error
#         error_text = "<p>The error:<br>" + str(e) + "</p>"
#         hed = '<h1>Something is broken.</h1>'
#         return hed + error_text

# def MagerDicts(dict1, dict2):
#     if isinstance(dict1, list) and isinstance(dict2, list):
#         return dict1 + dict2
#     if isinstance(dict1, dict) and isinstance(dict2, dict):
#         return dict(list(dict1.items()) + list(dict2.items()))
#
#
# @invoice_module.route('/', methods=['GET', 'POST'])
# @login_required
# def viewCart():
#     if current_user.is_authenticated:
#         if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
#             return redirect('/')
#         subtotal = 0
#         grandtotal = 0
#         for key, product in session['Shoppingcart'].items():
#             discount = (product['discount'] / 100) * float(product['price'])
#             subtotal += float(product['price']) * int(product['quantity'])
#             subtotal -= discount
#             tax = ("%.2f" % (.06 * float(subtotal)))
#             grandtotal = float("%.2f" % (1.06 * subtotal))
#
#         return render_template('cart.html', user=current_user, tax=tax, grandtotal=grandtotal)
#     return redirect('/')
#
#
# @invoice_module.route('/add-cart', methods=['POST'])
# @login_required
# def addCart():
#     try:
#         product_id = request.form.get('product_id')
#         quantity = int(request.form.get('quantity'))
#         color = request.form.get('colors')
#         product = Product.query.filter_by(id=product_id).first()
#         # product = Product.query(Product).filter_by(id=product_id).first()
#
#         if request.method == "POST":
#             dictItems = {product_id: {
#                 'name': product.name,
#                 'price': float(product.price),
#                 'discount': product.discount,
#                 'color': color,
#                 'quantity': quantity,
#                 'colors': product.colors}}
#
#             if 'Shoppingcart' in session:
#                 print(session['Shoppingcart'])
#                 if product_id in session['Shoppingcart']:
#                     for key, item in session['Shoppingcart'].items():
#                         if int(key) == int(product_id):
#                             session.modified = True
#                             item['quantity'] += 1
#                 else:
#                     session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], dictItems)
#                     return redirect(request.referrer)
#
#             else:
#                 session['Shoppingcart'] = dictItems
#                 return redirect(request.referrer)
#
#     except Exception as e:
#         print(e)
#     finally:
#         return redirect(request.referrer)
#
#
# @invoice_module.route('/update/<int:code>', methods=['POST'])
# def updateCart(code):
#     if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
#         return redirect(url_for('/'))
#     if request.method == "POST":
#         quantity = int(request.form.get('quantity'))
#
#         color = request.form.get('colors')
#         try:
#             session.modified = True
#             for key, item in session['Shoppingcart'].items():
#                 if int(key) == code:
#                     item['quantity'] = quantity
#                     item['color'] = color
#                     flash('Item is updated!')
#                     return redirect(url_for('cart.viewCart'))
#         except Exception as e:
#             print(e)
#             return redirect(url_for('cart.viewCart'))
#
#
# @invoice_module.route('/delete-item/<int:id>')
# def deleteItem(id):
#     if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
#         return redirect(url_for('/'))
#     try:
#         session.modified = True
#         for key, item in session['Shoppingcart'].items():
#             if int(key) == id:
#                 session['Shoppingcart'].pop(key, None)
#                 return redirect(url_for('cart.viewCart'))
#     except Exception as e:
#         print(e)
#         return redirect(url_for('cart.viewCart'))
#
#
# @invoice_module.route('/clearcart')
# def clearcart():
#     try:
#         session.pop('Shoppingcart', None)
#         return redirect(url_for('/'))
#     except Exception as e:
#         print(e)
#         return redirect(url_for('cart.viewCart'))
