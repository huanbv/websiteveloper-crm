from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required, current_user

from src import db
from src.main.modules.currency import Currency

from src.main.modules.currency.forms import CurrencyForm

currency_module = Blueprint('currency', __name__, static_folder='static', template_folder='templates')


@currency_module.route('/', methods=['GET', 'POST'])
@login_required
def currency():
    if current_user.is_authenticated:
        return render_template('currency.html', user=current_user)
    else:
        return redirect('/')
