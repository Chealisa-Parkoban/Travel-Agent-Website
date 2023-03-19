import wtforms
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL
from models import EmailCaptchaModel, User


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
    remember_me = BooleanField('REMEMBER ME')
    # admin
    is_admin = BooleanField('ADMIN')
    # submit the form
    submit = SubmitField('')


# form for sign up page
class SignupForm(FlaskForm):
    """Sign up for a user account."""
    username = StringField(
        'USERNAME',
        validators=
        [
            # validate the username, the length must longer than 4 characters
            # if the data is not valid, then shows the error message
            Length(min=4, message='Minimum username of four characters.'),
            DataRequired()
        ]
    )

    email = StringField(
        'EMAIL',
        validators=
        [
            # the format of the email address must be xxx@xxx.xx
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )

    email_verification_code = StringField(
        'VERIFICATION CODE',
        validators=
        [
            DataRequired()
        ]
    )

    password = PasswordField(
        'PASSWORD',
        validators=
        [
            Length(min=4, message='Minimum password of four characters.'),
            DataRequired(message="Please enter a password."),
        ]
    )
    confirm_password = PasswordField(
        'REENTER PASSWORD',
        validators=
        [
            EqualTo('password', message='Passwords must match.'),
            DataRequired(message="Please reenter the password.")
        ]
    )

    # recaptcha = RecaptchaField()
    submit = SubmitField('')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() == captcha.lower():
            # 首先这个email是否存在其次这个email对应的captcha是不是和user输入的captcha一样
            raise wtforms.ValidationError("邮箱验证码错误！")

    def validate_email(self, field):
        email = field.data
        user_model = User.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("邮箱已经存在！")


class CommentForm(FlaskForm):
    """Form for users to add/update a comment."""
    comment = StringField(
        'COMMENT',
        validators=
        [
            DataRequired()
        ]
    )
    submit = SubmitField('')

    def validate_comment(self, field):
        comment = field.data
        if len(comment) > 500:
            raise wtforms.ValidationError("Comment is too long.")



