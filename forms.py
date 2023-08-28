from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, SelectField, StringField
from wtforms.validators import DataRequired


class QRCodeForm(FlaskForm):
    """Form to gather data to generate qr code"""

    content = StringField("Content", validators=[DataRequired()])
    size = StringField("Size", default="200x200")
    charset_source = RadioField("Charset Source", choices=[("ISO-8859-1", "ISO-8859-1"), ("UTF-8", "UTF-8")], default="UTF-8")
    charset_target = RadioField("Charset Target", choices=[("ISO-8859-1", "ISO-8859-1"), ("UTF-8", "UTF-8")], default="UTF-8")
    ecc = SelectField("Error Correction Code", choices=[("L", "L"), ("M", "M"), ("Q", "Q"), ("H", "H")], default="L")
    color = StringField("Color", default="0-0-0")
    bg_color = StringField("Background Color", default="0-0-0")
    margin = IntegerField("Margin", default=1)
    qzone = IntegerField("Margin Thickness", default=0)
    file_format = RadioField("File Format", choices=[("png", "png"), ("gif", "gif"), ("jpeg", "jpeg"), ("jpg", "jpg"), ("svg", "svg"), ("eps", "eps")], default="png")
