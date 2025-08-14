from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    in_stock = BooleanField('In Stock')
    description = TextAreaField('Description')
    submit = SubmitField('Save')
