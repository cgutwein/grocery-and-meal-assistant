from prototype import app
from shutil import copyfile
from flask import render_template, flash, redirect, request
from prototype.forms import LoginForm, RegistrationForm, PreferencesForm, GrocerySearchForm, GroceryListForm, RecipeGenForm
from flask_login import current_user, login_user, logout_user, login_required
from prototype.models import User, Listdb, GroceryList
from werkzeug.urls import url_parse
from prototype import db
from werkzeug import secure_filename
from sqlalchemy import exists
import tablib
import os
from prototype.custom_functions import grocery, recipe
import pandas as pd
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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
        user.list_initialize()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('edit_profile')
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
        lists = Listdb.query.filter(Listdb.user_id == current_user.id)
        q = lists.filter(Listdb.list_name == current_user.current_list)
        if current_user.current_list != None:
            mylist = grocery.load_list_table(q[0].file_name)
        else:
            mylist = "You need to add items to your list."
        if form.validate_on_submit():
            ingredients = pd.read_csv('../python/data/ingredients_short.csv')
            series = ingredients['stem']
            table_string = grocery.ingr_search(form.query.data, series)
            if table_string == []:
                table_string = "No results generated from search.Try again."
            return render_template('grocery.html', title='Grocery List - Current', form=form, table_string=table_string, mylist=mylist)
        return render_template('grocery.html', title='Grocery List - Current', form=form, mylist=mylist)
    else:
        return redirect('/index')

@app.route('/grocery_list', methods=['GET', 'POST'])
def grocery_list():
    if current_user.is_authenticated:
        form = GroceryListForm()
        lists_table = "You do not have any saved lists."
        mylist = "You need to add items to the list."
        if db.session.query(exists().where(Listdb.user_id == current_user.id)).scalar():
            lists = Listdb.query.filter(Listdb.user_id == current_user.id)
            lists_table = grocery.load_groc_list(lists)
            if current_user.current_list != None:
                q = lists.filter(Listdb.list_name == current_user.current_list)
                if q:
                    mylist = grocery.load_list_table(q[0].file_name)
        if form.validate_on_submit():
            ob_list = GroceryList(name=form.new_name.data, user_id=current_user.username)
            list = Listdb(shopper=current_user, list_name = form.new_name.data, file_name=ob_list.filename)
            current_user.current_list = list.list_name
            db.session.add(list)
            db.session.commit()
            ob_list.save_list()
            return redirect('/grocery_list')
        return render_template('grocery_list.html', title='Grocery List - Current', form=form, lists_table=lists_table, mylist=mylist)
    else:
        return redirect('/index')

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if current_user.is_authenticated:
        form = RecipeGenForm()
        if form.validate_on_submit():
            q = Listdb.query.filter(Listdb.list_name == current_user.current_list).filter(Listdb.user_id == current_user.id)
            groceries = grocery.load_list(q[0].file_name).groc_list
            dof = form.dof.data
            meal_type = form.meal_type.data
            sort_field = form.sorting_field.data
            if current_user.daily_cal:
                recs = recipe.return_recipes(calories = current_user.daily_cal, protein = current_user.protein, fat = current_user.fat, carb = current_user.carb, complexity = current_user.complexity, cuisine=current_user.cuisine, n_additional_ingredients=dof, meal_type=meal_type, grocery=groceries, sort_field=sort_field)
            else:
                recs = "Please complete your user profile to see recipe recommendations."
            if len(recs) == 0:
                return render_template('recipes.html', title='Grocery List - Current', form=form)
            return render_template('recipes.html', title='Grocery List - Current', form=form, recs=recs)
        return render_template('recipes.html', title='Recepticon Recommendations', form=form)
    else:
        return redirect('/index')

@app.route('/add_item/<string:food_item>', methods=['POST'])
def add_food_item(food_item):
    q = Listdb.query.filter(Listdb.list_name == current_user.current_list).filter(Listdb.user_id == current_user.id)
    ob_list = grocery.load_list(q[0].file_name)
    ob_list.add_item(food_item)
    ob_list.save_list()
    return redirect('/grocery')

@app.route('/del_item/<string:food_item>', methods=['POST'])
def del_food_item(food_item):
    q = Listdb.query.filter(Listdb.list_name == current_user.current_list).filter(Listdb.user_id == current_user.id)
    ob_list = grocery.load_list(q[0].file_name)
    ob_list.delete_item(food_item)
    ob_list.save_list()
    return redirect('/grocery')

@app.route('/load_list/<string:f_list>', methods=['POST'])
def f_load_list(f_list):
    current_user.current_list = f_list
    db.session.commit()
    return redirect('/grocery_list')

@app.route('/del_list/<string:f_list>', methods=['POST'])
def f_del_list(f_list):
    q = Listdb.query.filter(Listdb.list_name == f_list).filter(Listdb.user_id == current_user.id)
    if os.path.exists(q[0].file_name):
      os.remove(q[0].file_name)
    else:
      print("The file does not exist")
    q.delete()
    current_user.current_list = None
    db.session.commit()
    return redirect('/grocery_list')

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    #### fill form in here
    return render_template('user.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = PreferencesForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.age = form.userage.data
        current_user.height = form.userheight.data
        current_user.weight = form.userweight.data
        current_user.gender = form.usergender.data
        current_user.gym = int(form.usergym.data)
        current_user.goals = int(form.usergoals.data)
        current_user.restrictions = form.userspecs.data
        current_user.cuisine = str(form.usercuisine.data)
        current_user.complexity = int(form.usercomplex.data)
        current_user.recipe_file = form.userrecipe.data
        current_user.about_me = form.about_me.data
        current_user.nutrigen()
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect('/edit_profile')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.userage.data = current_user.age
        form.userheight.data = current_user.height
        form.userweight.data = current_user.weight
        form.usergender.data = current_user.gender
        form.usergym.data = str(current_user.gym)
        form.usergoals.data = str(current_user.goals)
        form.userspecs.data = current_user.restrictions
        form.usercuisine.data = current_user.cuisine
        form.usercomplex.data = str(current_user.complexity)
        current_user.recipe_file = form.userrecipe.data
    return render_template('edit_profile.html', title='Edit Profile', form=form)
