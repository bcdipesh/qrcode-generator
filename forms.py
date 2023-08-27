from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, SelectField, StringField
from wtforms.validators import DataRequired


class QRCodeForm(FlaskForm):
    """Form to gather data to generate qr code"""

    content = StringField("Content", validators=[DataRequired()])
    size = StringField("Size")
    charset_source = RadioField("Charset Source", choices=[("ISO-8859-1", "ISO-8859-1"), ("UTF-8", "UTF-8")], default="UTF-8")
    charset_target = RadioField("Charset Target", choices=[("ISO-8859-1", "ISO-8859-1"), ("UTF-8", "UTF-8")], default="UTF-8")
    ecc = SelectField("Error Correction Code", choices=[("L", "L"), ("M", "M"), ("Q", "Q"), ("H", "H")], default="L")
    color = StringField("Color")
    bg_color = StringField("Background Color")
    margin = IntegerField("Margin")
    qzone = IntegerField("Margin Thickness")
    file_format = RadioField("File Format", choices=[("PNG", "png"), ("GIF", "gif"), ("JPEG", "jpeg"), ("JPG", "jpg"), ("SVG", "svg"), ("EPS", "eps")], default="PNG")
