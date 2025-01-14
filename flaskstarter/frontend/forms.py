# -*- coding: utf-8 -*-

from flask import Markup

from flask_wtf import FlaskForm
from wtforms import (ValidationError, HiddenField, BooleanField, TextField,
                     PasswordField, SubmitField, TextAreaField)
from wtforms.validators import Required, Length, EqualTo, Email
from wtforms.fields.html5 import EmailField

from ..utils import (NAME_LEN_MIN, NAME_LEN_MAX, PASSWORD_LEN_MIN,
                     PASSWORD_LEN_MAX)

from ..user import Users

terms_html = Markup('<a target="blank" href="#">Terms of Service</a>')

forgotpassword_html = Markup('<a href="/reset_password" class="text-muted float-end"><small>Forgot your password?</small></a>')


class LoginForm(FlaskForm):
    next = HiddenField()
    login = TextField(u'Email', [Required()])
    password = PasswordField('Password', [Required(),
                                          Length(PASSWORD_LEN_MIN,
                                                 PASSWORD_LEN_MAX)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class SignupForm(FlaskForm):
    next = HiddenField()
    name = TextField(u'Name', [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)])
    email = EmailField(u'Email', [Required(), Email()])
    password = PasswordField(u'Password' ,
                             [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
                             description=u' 6 or more characters.')
    agree = BooleanField(u'I Agree to the ' + terms_html, [Required()])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken')


class RecoverPasswordForm(FlaskForm):
    email = EmailField(u'Your email', [Email()])
    submit = SubmitField('Send instructions')


class ChangePasswordForm(FlaskForm):
    email_activation_key = HiddenField()
    email = HiddenField()
    password = PasswordField(u'Password', [Required()])
    password_again = PasswordField(u'Password again', [EqualTo('password', message="Passwords don't match")])
    submit = SubmitField('Save')


class ContactUsForm(FlaskForm):
    name = TextField(u'Name', [Required(), Length(max=64)])
    email = EmailField(u'Your Email', [Required(), Email(), Length(max=64)])
    subject = TextField(u'Subject', [Required(), Length(5, 128)])
    message = TextAreaField(u'Your Message', [Required(), Length(10, 1024)])
    submit = SubmitField('Submit')
