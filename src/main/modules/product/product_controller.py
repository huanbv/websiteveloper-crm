from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user

from src import db
from src.main.modules.product import ProductBrand, ProductCategory

from src.main.modules.product.forms import ProductBrandForm, ProductCategoryForm, ProductForm


product_module = Blueprint('product', __name__, static_folder='static', template_folder='templates')


@product_module.route('/', methods=['GET', 'POST'])
@login_required
def product():
    if current_user.is_authenticated:
        return render_template('product.html', user=current_user)
    return redirect('/')


@product_module.route('/add', methods=['GET', 'POST'])
@login_required
def addProduct():

    form = ProductForm()

    product_brands = ProductBrand.query.all()
    product_categories = ProductCategory.query.all()

    if form.validate_on_submit():

        text = form.inputName.data

        the_brand = ProductBrand(text=text)

        db.session.add(the_brand)
        db.session.commit()
        return redirect('/product')

    return render_template('add-product.html', form=form, product_brands=product_brands,
                           product_categories=product_categories)


@product_module.route('brand/add', methods=['GET', 'POST'])
@login_required
def addProductBrand():

    form = ProductBrandForm()

    if form.validate_on_submit():

        text = form.inputName.data

        the_brand = ProductBrand(text=text)

        db.session.add(the_brand)
        db.session.commit()
        return redirect('/product')

    return render_template('add-product-brand.html', form=form, product_brands='product_brands')


@product_module.route('category/add', methods=['GET', 'POST'])
@login_required
def addProductCategory():

    form = ProductCategoryForm()

    if form.validate_on_submit():

        text = form.inputName.data

        the_category = ProductCategory(text=text)

        db.session.add(the_category)
        db.session.commit()
        return redirect('/product')

    return render_template('add-product-brand.html', form=form)
