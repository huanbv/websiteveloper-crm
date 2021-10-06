from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required, current_user

from src import db
from src.main.modules.contact import Contact, Gender

from src.main.modules.contact.forms import ContactForm


contact_module = Blueprint('contact', __name__, static_folder='static', template_folder='templates')


@contact_module.route('/', methods=['GET', 'POST'])
@login_required
def contact():
    if current_user.is_authenticated:
        return render_template('contact.html', user=current_user)
    return redirect('/')
