# app/routes.py

from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timezone
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PetForm, PagamentoForm
from app.models import User, Pet, Pagamento

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
def index():
    
    return render_template("index.html", title='Pagina inicial')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Login Page", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            telefone=form.telefone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='EditProfile', form=form)

@app.route('/profile_items', methods=['GET', 'POST'])
@login_required
def profile_items():
    pet_form = PetForm()
    pagamento_form = PagamentoForm()

    # Processa envio do formulário de Pet
    if pet_form.submit_pet.data and pet_form.validate_on_submit():
        new_pet = Pet(
            nome=pet_form.nome.data,
            peso=pet_form.peso.data,
            sangue=pet_form.sangue.data,
            idade=pet_form.idade.data,
            raca=pet_form.raca.data,
            especie=pet_form.especie.data,
            pelagem=pet_form.pelagem.data,
            sexo=pet_form.sexo.data,
            user_id=current_user.id
        )
        db.session.add(new_pet)
        db.session.commit()
        flash('Pet adicionado com sucesso!')
        return redirect(url_for('profile_items'))

    # Processa envio do formulário de Pagamento
    if pagamento_form.submit_pagamento.data and pagamento_form.validate_on_submit():
        new_pagamento = Pagamento(
            data=pagamento_form.data_pagamento.data,
            tipo=pagamento_form.tipo.data,
            user_id=current_user.id
        )
        db.session.add(new_pagamento)
        db.session.commit()
        flash('Pagamento adicionado com sucesso!')
        return redirect(url_for('profile_items'))

    # Recupera os registros do usuário logado:
    pets = current_user.pets.all()
    pagamentos = current_user.pagamentos.all()

    return render_template('profile_items.html',
                           pet_form=pet_form,
                           pagamento_form=pagamento_form,
                           pets=pets,
                           pagamentos=pagamentos)