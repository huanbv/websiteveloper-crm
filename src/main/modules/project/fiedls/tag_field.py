from wtforms.fields import SelectMultipleField


class TagField(SelectMultipleField):
    def __init__(self, **kwargs):
        super(TagField, self).__init__(**kwargs)

        self.coerce = int

        self.label.text = "Tags"

        from src.main.modules.tag.tag_model import Tag
        self.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
