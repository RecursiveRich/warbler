from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea


class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    image_url = StringField('image_url')
    password = PasswordField('password', validators=[Length(min=6)])
    name = StringField('name')
    location = StringField('location')
    bio = StringField('bio', validators=[Length(max=140)], widget=TextArea())
    header_image_url = StringField('header image url')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[Length(min=6)])
