from prototype import app
from shutil import copyfile
from flask import render_template, flash, redirect, request
from prototype.forms import LoginForm, RegistrationForm, PreferencesForm, GrocerySearchForm
from flask_login import current_user, login_user, logout_user, login_required
from prototype.models import User
from werkzeug.urls import url_parse
from prototype import db
from werkzeug import secure_filename
import tablib
import os
from prototype.custom_functions import grocery
import pandas as pd

@app.route('/')
@app.route('/home')
@app.route('/index')
@login_required
def index():
    form = PreferencesForm()
    if form.validate_on_submit():
        age = form.userage.data
        height = form.userheight.data
        weight = form.userweight.data
        gender = form.usergender.data
        gym = form.usergym.data
        goals = form.usergoals.data
        restrictions = form.userspecs.data
        cuisine = form.usercuisine.data
        complexity = form.usercomplex.data
        day_meal = form.usermeal.data
        recipe_file = form.userrecipe.data
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/results'
        return redirect(next_page)
        return redirect('/results')
    return render_template('index.html', title='Home', form=form)

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
def results():
   if request.method == 'POST':
      usr_gym = request.form['usergym']
      f = request.files['userrecipe']
      f.save(secure_filename(f.filename))
      result_page = mycopy(f.filename)
      return render_template('results.html', title='Results', usr_gym=usr_gym)

@app.route('/grocery', methods=['GET', 'POST'])
def grocery_list_gen():
    if current_user.is_authenticated:
        form = GrocerySearchForm()
        if form.validate_on_submit():
            ingredients = pd.read_csv('../python/files/ingr_list.csv')
            series = ingredients['ingredient']
            table_string = grocery.ingr_search(form.query.data, series)
            if table_string == []:
                table_string = "No results generated from search.Try again."
            return render_template('grocery.html', title='Grocery List - Current', form=form, table_string=table_string)
        return render_template('grocery.html', title='Grocery List - Current', form=form)
    else:
        return redirect('/index')

@app.route('/grocery_list', methods=['GET', 'POST'])
def grocery_list():
    if current_user.is_authenticated:
        return render_template('grocery_list.html', title='Grocery List - Current')
    else:
        return redirect('/index')
