from flask import Blueprint, render_template, redirect, request, url_for, current_app, flash
from flask_login import login_required, current_user

from src import db
from src.main.modules.product import ProductBrand, ProductCategory, Product

from src.main.modules.product.forms import ProductBrandForm, ProductCategoryForm, ProductForm


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


@product_module.route('edit/<int:id>', methods=['GET', 'POST'])
@login_required
def editProduct(id):
    form = ProductForm()
    # re-index product brand form product brand table
    # on get request -- showing the form view
    form.inputProductBrand.choices = [(p.id, p.text) for p in db.session.query(ProductBrand).all()]

    # re-index product category form product category table
    form.inputProductCategory.choices = [(p.id, p.text) for p in db.session.query(ProductCategory).all()]


    the_product = db.session.query(Product).get(id)
    if form.validate_on_submit():

        the_product.name = form.inputName.data
        the_product.price = form.inputPrice.data
        the_product.discount = form.inputDiscount.data
        the_product.stock = form.inputStock.data
        the_product.colors = form.inputColor.data
        the_product.description = form.inputDescription.data
        the_product.product_brand_id = form.inputProductBrand.data
        the_product.product_category_id = form.inputProductCategory.data

        db.session.commit()
        return redirect('/product')

    form.inputName.default = the_product.name
    form.inputPrice.default = the_product.price
    form.inputDiscount.default = the_product.discount
    form.inputStock.default = the_product.stock
    form.inputColor.default = the_product.colors
    form.inputDescription.default = the_product.description
    form.inputProductCategory.default = the_product.product_category_id

    form.process()

    return render_template('/add-product-brand.html', form=form, user=current_user)


@product_module.route('delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteProduct(id):
    the_product = db.session.query(Product).filter_by(id=id).first()
    db.session.delete(the_product)
    db.session.commit()
    return redirect(f"/product")


@product_module.route('brand/add', methods=['GET', 'POST'])
@login_required
def addProductBrand():

    form = ProductBrandForm()

    if form.validate_on_submit():

        text = form.inputName.data

        the_brand = ProductBrand(text=text)

        db.session.add(the_brand)
        db.session.commit()
        return redirect('/brand')

    return render_template('add-product-brand.html', form=form, product_brands='product_brands', user=current_user)


@product_module.route('/brand', methods=['GET', 'POST'])
@login_required
def productBrand():
    form = ProductBrandForm()

    if current_user.is_authenticated:
        if form.validate_on_submit():
            text = form.inputName.data

            the_brand = ProductBrand(text=text)
            db.session.add(the_brand)
            db.session.commit()
            return redirect('/product/brand')

        product_brands = ProductBrand.query.all()
        return render_template('product-brand.html', user=current_user, product_brands=product_brands, form=form)
    return redirect('/')


@product_module.route('brand/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def editProductBrand(id):
    form = ProductBrandForm()

    the_brand = db.session.query(ProductBrand).get(id)
    if form.validate_on_submit():

        the_brand.text = form.inputName.data

        db.session.commit()
        return redirect('/product/brand')

    form.inputName.default = the_brand.text

    form.process()

    return render_template('/add-product-brand.html', form=form, user=current_user)


@product_module.route('brand/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteProductBrand(id):
    the_product_brand = db.session.query(ProductBrand).filter_by(id=id).first()
    db.session.delete(the_product_brand)
    db.session.commit()
    return redirect(f"/product/brand")


@product_module.route('category/add', methods=['GET', 'POST'])
@login_required
def addProductCategory():

    form = ProductCategoryForm()

    if form.validate_on_submit():

        text = form.inputName.data

        the_category = ProductCategory(text=text)

        db.session.add(the_category)
        db.session.commit()
        return redirect('/product/category')

    return render_template('add-product-brand.html', form=form, user=current_user)


@product_module.route('/category', methods=['GET', 'POST'])
@login_required
def productCategory():
    form = ProductCategoryForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            text = form.inputName.data
            the_category = ProductCategory(text=text)
            db.session.add(the_category)
            db.session.commit()
            return redirect('/product/category')

        product_categories = ProductCategory.query.all()
        return render_template('product-category.html', user=current_user, product_categories=product_categories,
                               form=form)
    return redirect('/')



@product_module.route('category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def editProductCategory(id):
    form = ProductCategoryForm()

    the_category = db.session.query(ProductCategory).get(id)
    if form.validate_on_submit():

        the_category.text = form.inputName.data

        db.session.commit()
        return redirect('/product/category')

    form.inputName.default = the_category.text

    form.process()

    return render_template('/add-product-brand.html', form=form, user=current_user)


@product_module.route('category/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteProductCategory(id):
    the_product_category = db.session.query(ProductCategory).filter_by(id=id).first()
    db.session.delete(the_product_category)
    db.session.commit()
    return redirect(f"/product/category")
