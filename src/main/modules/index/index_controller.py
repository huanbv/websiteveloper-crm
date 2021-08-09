from flask import Blueprint, render_template

index_module = Blueprint('index', __name__, static_folder='static', template_folder='templates')


@index_module.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

