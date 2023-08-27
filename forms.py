from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, IntegerField
from wtforms.validators import DataRequired


class QRCodeForm(FlaskForm):
    """Form to gather data to generate qr code"""

    data = StringField("Data", validators=[DataRequired()])
    size = StringField("Size")
    charset_source = RadioField("Charset Source")
    charset_target = RadioField("Charset Target")
    ecc = SelectField("Error Correction Code")
    color = StringField("Color")
    bg_color = StringField("Background Color")
    margin = IntegerField("Margin")
    qzone = IntegerField("Margin Thickness")
    format = RadioField("File Format")
