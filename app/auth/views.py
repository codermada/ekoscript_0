import os, shutil

from flask import render_template, flash, redirect, url_for, current_app

from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from .forms import LoginForm, RegisterForm

from .. import db
from ..models import User
from config import basedir

@auth.route('/')
def index():
    return render_template('auth/index.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username
        password = form.password.data
        user = User(username=username.data, password=password)
        db.session.add(user)
        db.session.commit()
        flash(f'{user.username} registered successfully.')
        return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            if not os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id))):
                os.mkdir(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)))
            return redirect(url_for('main.index'))
        flash('Invalid username or password.')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id))):
        shutil.rmtree(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)))
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))