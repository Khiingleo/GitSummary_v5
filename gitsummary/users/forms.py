"""Form fields"""
from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import DataRequired, length, Email, EqualTo
from gitsummary.models import User
import email_validator


class RegistrationForm(FlaskForm):
    """registration form"""
    username = StringField('Username',
                           validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), length(min=2, max=18)])
    confirm_password = PasswordField("Confirm Password",
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise validators.ValidationError('That username is already in use. Please choose another one')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise validators.ValidationError('That email is already in use. Please choose another one')
    
  
class LoginForm(FlaskForm):
    """login form"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), length(min=2, max=18)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    """registration form"""
    username = StringField('Username',
                           validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise validators.ValidationError('That username is already in use. Please choose another one')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise validators.ValidationError('That email is already in use. Please choose another one')
            

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise validators.ValidationError('There is no account with that email. Please register first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",
                             validators=[DataRequired(), length(min=2, max=18)])
    confirm_password = PasswordField("Confirm Password",
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")