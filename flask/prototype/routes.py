from prototype import app
from shutil import copyfile
from flask import render_template, flash, redirect, request
from prototype.forms import LoginForm, RegistrationForm, PreferencesForm, GrocerySearchForm, GroceryListForm, RecipeGenForm
from flask_login import current_user, login_user, logout_user, login_required
from prototype.models import User, Listdb, GroceryList
from werkzeug.urls import url_parse
from prototype import db
from werkzeug import secure_filename
import tablib
import os
from prototype.custom_functions import grocery, recipe
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
            ingredients = pd.read_csv('../python/data/ingredients_short.csv')
            series = ingredients['stem']
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
        form = GroceryListForm()
        if form.validate_on_submit():
            ob_list = GroceryList(name=form.new_name.data, user_id=current_user.username)
            list = Listdb(shopper=current_user, list_name = form.new_name.data, file_name=ob_list.filename)
            current_user.current_list = list.list_name
            db.session.add(list)
            db.session.commit()
            ob_list.save_list()
            return redirect('/grocery_list')
        lists = Listdb.query.filter(Listdb.user_id == current_user.id)
        lists_table = grocery.load_groc_list(lists)
        q = lists.filter(Listdb.list_name == current_user.current_list)
        if current_user.current_list != None:
            mylist = grocery.load_list_table(q[0].file_name)
        else:
            mylist = "You need to add items to your list."
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
            recs = recipe.return_recipes(n_additional_ingredients=dof, grocery=groceries)
            if recs == "":
                recs = "No results generated from search.Try again."
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
    return redirect('/grocery_list')

@app.route('/load_list/<string:f_list>', methods=['POST'])
def f_load_list(f_list):
    current_user.current_list = f_list
    db.session.commit()
    return redirect('/grocery_list')

@app.route('/del_list/<string:f_list>', methods=['POST'])
def f_del_list(f_list):
    q = Listdb.query.filter(Listdb.list_name == f_list).filter(Listdb.user_id == current_user.id)
    import os
    if os.path.exists(q[0].file_name):
      os.remove(q[0].file_name)
    else:
      print("The file does not exist")
    q.delete()
    db.session.commit()
    return redirect('/grocery_list')
