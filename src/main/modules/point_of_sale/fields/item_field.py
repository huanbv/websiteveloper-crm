from wtforms.fields import SelectMultipleField


class ItemField(SelectMultipleField):
    def __init__(self, **kwargs):
        super(ItemField, self).__init__(**kwargs)

        self.coerce = int

        self.label.text = "Items"

        from src.main.modules.product.product_model import Product
        self.choices = [(product.id, product.name) for product in Product.query.all()]
