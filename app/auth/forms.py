from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, EmailField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo


class AuthForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired( message='Username needed'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                            'Usernames must have only letters, '
                                                                     'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired( message='Password needed'), Length(0, 50)])


class RegisterForm(AuthForm):
    password2 = PasswordField('Confirm password', validators=[DataRequired( message='Please confirm password'), 
                                                            Length(0, 50),
                                                            EqualTo('password', message='Password must match')])
    submit = SubmitField('Sign up')


class LoginForm(AuthForm):
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign in')