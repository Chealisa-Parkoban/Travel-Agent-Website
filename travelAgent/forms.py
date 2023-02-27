from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL


# Using FlaskForm to collect data from user
# Using FlaskForm's validators to validate users' input
# This is called data validation
class LoginForm(FlaskForm):
    # Validator here requires user must have input data
    # username is String
    username = StringField('USERNAME', validators=[Length(min=4), DataRequired()])
    # password should be represented in password form
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    # choose to remember the info or not
    # remember_me = BooleanField('REMEMBER ME')
    # submit the form
    submit = SubmitField('')