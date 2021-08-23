from flask import Blueprint, render_template
from flask_login import login_required, current_user

index_module = Blueprint('index', __name__, static_folder='static', template_folder='templates')


@index_module.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template("index-admin.html", user=current_user)

    return render_template("index.html")


@index_module.route('auth/dashboard', methods=['GET', 'POST'])
@login_required
def indexAdmin():
    return render_template("index-admin.html")


@index_module.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
