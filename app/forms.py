#   app/forms.py

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, BooleanField, SubmitField, DateField, FloatField, IntegerField
from wtforms.validators import Length, ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
import phonenumbers
from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_telefone(self, telefone):
        try:
            phone = phonenumbers.parse(telefone.data, "BR")  # Altere para o país desejado
            if not phonenumbers.is_valid_number(phone):
                raise ValidationError("Número de telefone inválido.")
        except:
            raise ValidationError("Formato de telefone inválido.")

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class PetForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    peso = FloatField('Peso (kg)', validators=[DataRequired()])
    sangue = StringField('Sangue', validators=[DataRequired()])
    idade = IntegerField('Idade (em anos)', validators=[DataRequired()])
    raca = StringField('Raça', validators=[DataRequired()])
    especie = StringField('Espécie', validators=[DataRequired()])
    pelagem = StringField('Pelagem', validators=[DataRequired()])
    sexo = StringField('Sexo', validators=[DataRequired()])
    submit_pet = SubmitField('Adicionar Pet')

class PagamentoForm(FlaskForm):
    data_pagamento = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    tipo = StringField('Tipo', validators=[DataRequired()])
    submit_pagamento = SubmitField('Adicionar Pagamento')