from flask import Blueprint, render_template, flash, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import redirect

from src import db
from .forms import LoginForm, SignupForm
from src.main.modules.user import User

auth_module = Blueprint('auth', __name__, static_folder='static', template_folder='templates')


@auth_module.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # the form is fulfilled
    if form.validate_on_submit():
        the_user = User.query.get(form.email.data)

        # the user is exists
        if the_user:

            # check whether the user's entered password is matched
            if the_user.check_password_hash(form.password.data):
                login_user(the_user)

                # kiem tra role va chuyen huong theo quyen
                return redirect('dashboard')
                # return render_template("index-admin.html", form=form)

            flash('Password was wrong')
            return render_template("login.html", form=form)

        flash('User not registered')
        return render_template("login.html", form=form)

    flash('Please fill out the form')
    return render_template("login.html", form=form)


@auth_module.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    # the form is fulfilled
    if form.validate_on_submit():
        is_old_user_exist = User.query.get(form.email.data) is not None

        if not is_old_user_exist:
            the_user = User(
                email=form.email.data,
                raw_password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )

            db.session.add(the_user)
            db.session.commit()

            flash('Successfully registered')
            return redirect(url_for('auth.login'))

        form.email.errors.append('The user with this email is already registered')
        # flash('The user with this email is already registered')
        return render_template("signup.html", form=form)

    flash('Please fill out the form')
    return render_template("signup.html", form=form)


@auth_module.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('auth.login'))
