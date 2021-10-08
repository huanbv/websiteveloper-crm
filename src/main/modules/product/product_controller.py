from flask import Blueprint, render_template, redirect, request, url_for, current_app, flash
from flask_login import login_required, current_user

from src import db
from src.main.modules.product import ProductBrand, ProductCategory, Product

from src.main.modules.product.forms import ProductBrandForm, ProductCategoryForm, ProductForm

import secrets

product_module = Blueprint('product', __name__, static_folder='static', template_folder='templates')


@product_module.route('/', methods=['GET', 'POST'])
@login_required
def product():
    if current_user.is_authenticated:
        products = Product.query.all()
        return render_template('product.html', user=current_user, products=products)
    return redirect('/')


@product_module.route('/add', methods=['GET', 'POST'])
@login_required
def addProduct():

    form = ProductForm()

    # select product brand status form product brand table
    form.inputProductBrand.choices = [(p.id, p.text) for p in db.session.query(ProductBrand).all()]
    form.inputProductCategory.choices = [(p.id, p.text) for p in db.session.query(ProductCategory).all()]


    if form.validate_on_submit():
        if request.method == "POST":

            name = form.inputName.data
            price = form.inputPrice.data
            discount = form.inputDiscount.data
            stock = form.inputStock.data
            colors = form.inputColor.data
            description = form.inputDescription.data
            product_brand_id = form.inputProductBrand.data
            product_category_id = form.inputProductCategory.data

            the_product = Product(name=name, price=price, discount=discount, stock=stock, colors=colors,
                                  description=description, product_brand_id=product_brand_id,
                                  product_category_id=product_category_id)

            db.session.add(the_product)
            db.session.commit()
            flash('Your product has been submitted', 'success')
            return redirect('/product')

    return render_template('add-product.html', form=form, user=current_user)


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
