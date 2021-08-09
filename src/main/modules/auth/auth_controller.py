from flask import Blueprint, render_template

from .forms import LoginForm, SignupForm


auth_module = Blueprint('auth', __name__, static_folder='static', template_folder='templates')


@auth_module.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)
