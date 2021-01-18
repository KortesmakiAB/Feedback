from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField
# from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, Email, Length

class AddUserForm(FlaskForm):
    """Form for adding a pet."""

    username    = StringField('Username', validators = [InputRequired(), Length(max = 20)])
    password    = PasswordField('Password', validators = [InputRequired()])
    email       = StringField('Email Address', validators = [InputRequired(), Length(max = 50), Email()])
    first_name  = StringField('First Name', validators = [InputRequired(), Length(max = 30)])
    last_name   = StringField('Last Name', validators = [InputRequired(), Length(max = 30)])


class LoginForm(FlaskForm):
    """Form for logging in."""

    username    = StringField('Username', validators = [InputRequired(), Length(max = 20)])
    password    = PasswordField('Password', validators = [InputRequired()])


class FeedbackForm(FlaskForm):
    """Form for submitting feedback."""

    title       = StringField('Title', validators = [InputRequired(), Length(max = 100)])
    content     = TextAreaField('Feedback', validators = [InputRequired()])