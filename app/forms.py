from operator import length_hint
from typing import Text
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.fields.core import DateField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import User
from flask_wtf.file import FileField


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

class RegistrationForm(FlaskForm):
    employee = SubmitField(_l('Employee'))
    employer = SubmitField(_l('Employer'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    
    upload_resume = SubmitField('Upload Your Resume')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class PostFormEmployer(FlaskForm):
    position_title = StringField(_l('Job Title'), validators=[DataRequired(), Length(min=0, max=30)], render_kw={"placeholder": "Required"})
    contact_phone = StringField(_l('Contact Number'), validators=[DataRequired(), Length(min=0, max=15)], render_kw={"placeholder": "Required"})
    physical_address = StringField(_l('Job Location'), validators=[DataRequired(), Length(min=0, max = 100)], render_kw={"placeholder": "Required"})
    body = TextAreaField(_l('Other Information and Requirements'), validators=[DataRequired(), Length(min=0,max=1000)])
    submit = SubmitField(_l('Submit'))

class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class ResumeForm(FlaskForm):
    resume = FileField('Upload')

class EditProfileFormEmployee(EditProfileForm):
    home_address = TextAreaField(_l('Home Address'), validators=[Length(min=0, max=140), DataRequired()])
    date_birth = DateField(_l('Date of Birth'), validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    location = TextAreaField(_l('City'), validators=[DataRequired(),Length(min=0, max=19)],)
    submit = SubmitField(_l('Submit'))

class RegistrationFormEveryone(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()], render_kw={"placeholder": "Required"})
    email = StringField(_l('Email (Note: Your profile picture will be synced with Gravatar)'), validators=[DataRequired(), Email()], render_kw={"placeholder": "Required"})
    password = PasswordField(_l('Password'), validators=[DataRequired()], render_kw={"placeholder": "Required"})
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')],render_kw={"placeholder": "Required"})
    contact_phone = StringField(_l('Contact Number'), validators=[DataRequired()], render_kw={"placeholder": "Required"})
    official_id = IntegerField(_l('Government ID Number'),validators=[DataRequired()], render_kw={"placeholder": "Required"})
    name = StringField(_l('Name'), validators=[DataRequired()], render_kw={"placeholder": "Required"})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))

class RegistrationFormEmployee(RegistrationFormEveryone):
    home_address = StringField(_l('Home Address'), validators=[Length(min=0, max=140), DataRequired()], render_kw={"placeholder": "Required"})
    date_birth = DateField(_l('Date of Birth'), validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    location = StringField(_l('City and Region'), validators=[DataRequired(),Length(min=0, max=19)],render_kw={"placeholder": "Required"})
    submit = SubmitField(_l('Submit'))

class RegistrationFormEmployer(RegistrationFormEveryone):
    legal_person_name = StringField(_l('Legal Agent Name'), validators=[Length(min=0, max=20),DataRequired()], render_kw={"placeholder": "Required"})
    legal_person_phone = StringField(_l('Legal Agent Contact Number'), validators=[Length(min=0, max=20),DataRequired()], render_kw={"placeholder": "Required"})
    physical_address = StringField(_l('Company Address'), validators=[Length(min=0, max=14),DataRequired()], render_kw={"placeholder": "Required"})
    submit = SubmitField(_l('Submit'))