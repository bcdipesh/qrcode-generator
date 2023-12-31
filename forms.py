from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, RadioField, SelectField,
                     StringField)
from wtforms.validators import DataRequired, Email, Length


class QRCodeForm(FlaskForm):
    """Form to gather data to generate qr code"""

    content = StringField("Content", validators=[DataRequired()])
    size = StringField("Size", default="200x200")
    charset_source = RadioField("Charset Source", choices=[("ISO-8859-1", "ISO-8859-1"), ("UTF-8", "UTF-8")], default="UTF-8")
    charset_target = RadioField("Charset Target", choices=[("ISO-8859-1", "ISO-8859-1"), ("UTF-8", "UTF-8")], default="UTF-8")
    ecc = SelectField("Error Correction Code", choices=[("L", "L"), ("M", "M"), ("Q", "Q"), ("H", "H")], default="L")
    color = StringField("Color", default="0-0-0")
    bg_color = StringField("Background Color", default="f-f-f")
    margin = IntegerField("Margin", default=1)
    qzone = IntegerField("Margin Thickness", default=0)
    file_format = RadioField("File Format", choices=[("png", "png"), ("gif", "gif"), ("jpeg", "jpeg"), ("jpg", "jpg"), ("svg", "svg")], default="png")


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class SignUpForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])

class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])