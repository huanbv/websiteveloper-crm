from flask import Blueprint, render_template, redirect, request, session, url_for, flash
from flask_login import login_required, current_user

from src.main.modules.product.product_model import Product

cart_module = Blueprint('cart', __name__, static_folder='static', template_folder='templates')


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@cart_module.route('/', methods=['GET', 'POST'])
@login_required
def viewCart():
    if current_user.is_authenticated:
        if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
            return redirect('/')
        subtotal = 0
        grandtotal = 0
        for key, product in session['Shoppingcart'].items():
            discount = (product['discount'] / 100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            tax = ("%.2f" % (.06 * float(subtotal)))
            grandtotal = float("%.2f" % (1.06 * subtotal))

        return render_template('cart.html', user=current_user, tax=tax, grandtotal=grandtotal)
    return redirect('/')


@cart_module.route('/add-cart', methods=['POST'])
@login_required
def addCart():
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


@cart_module.route('/update/<int:code>', methods=['POST'])
def updateCart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('/'))
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
                    return redirect(url_for('cart.viewCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('cart.viewCart'))


@cart_module.route('/delete-item/<int:id>')
def deleteItem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('/'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('cart.viewCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart.viewCart'))


@cart_module.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('/'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart.viewCart'))
