from prototype import app
from shutil import copyfile
from flask import render_template, flash, redirect, request
from prototype.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from prototype.models import User
from werkzeug.urls import url_parse
from prototype import db
from prototype.forms import RegistrationForm
from werkzeug import secure_filename
import tablib
import os

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/index'
        return redirect(next_page)
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('index')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('login')
    return render_template('register.html', title='Register', form=form)

def mycopy(fname):
   copyfile(fname, 'new_file.csv')
   dataset = tablib.Dataset()
   with open('new_file.csv') as f:
      dataset.csv = f.read()
   return dataset.html

@app.route('/results', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      radio_selection = request.form['user_options']
      list_selection = request.form['city']
      f = request.files['file']
      f.save(secure_filename(f.filename))
      result_page = mycopy(f.filename)
      return result_page
