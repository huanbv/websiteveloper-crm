from flask import Blueprint, render_template, redirect, flash, jsonify
from flask_login import login_required, current_user

from src import db
from src.main.modules.country.country_model import Country, State, City

from src.main.modules.country.forms import CountryForm

country_module = Blueprint('country', __name__, static_folder='static', template_folder='templates')


@country_module.route('/', methods=['GET', 'POST'])
@login_required
def country():
    if current_user.is_authenticated:

        form = CountryForm()
        form.country.choices = [(country.id, country.name) for country in Country.query.all()]
        form.process()
        return render_template('country.html', form=form, user=current_user)
    return redirect('/')


@country_module.route('/state/<get_state>')
@login_required
def stateByCountry(get_state):
    if current_user.is_authenticated:
        state = State.query.filter_by(country_id=get_state).all()
        stateArray = []
        for city in state:
            stateObj = {'id': city.id, 'name': city.name}

            stateArray.append(stateObj)

        return jsonify({'stateCountry': stateArray})


@country_module.route('/city/<get_city>')
@login_required
def city(get_city):
    if current_user.is_authenticated:
        state_data = City.query.filter_by(state_id=get_city).all()
        cityArray = []
        for city in state_data:
            cityObj = {'id': city.id, 'name': city.name}
            cityArray.append(cityObj)
        return jsonify({'cityList': cityArray})
