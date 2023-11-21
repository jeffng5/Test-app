from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email")
    first_name = StringField("first name")
    last_name = StringField("last name")

class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):

    title = StringField("title", validators=[InputRequired()])
    content = TextAreaField('content', validators=[InputRequired()])

