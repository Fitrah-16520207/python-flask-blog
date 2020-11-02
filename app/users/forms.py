from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.model import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',  validators=[DataRequired()])
    confirm_password = PasswordField('Konfirmasi Password',  validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username telah diambil. Silahkan buat username lainnya')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email telah diambil. Silahkan pilih email lainnya')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',  validators=[DataRequired()])
    remember = BooleanField('Ingat Saya')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    picture = FileField('Update Foto Profil', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update Akun')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username telah diambil. Silahkan buat username lainnya')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email telah diambil. Silahkan pilih email lainnya')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Minta Ubah Password')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Tidak ditemukan akun dengan Email tersebut. Harap registrasi terlebih dahulu')

class ResetPasswordForm(FlaskForm):
        password = PasswordField('Password',  validators=[DataRequired()])
        confirm_password = PasswordField('Konfirmasi Password',  validators=[DataRequired(),EqualTo('password')])
        submit = SubmitField('Ubah Password')