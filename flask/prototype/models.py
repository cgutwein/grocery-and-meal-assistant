from prototype import db, login
from prototype.custom_functions import nutrition
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_table import Table, Col, ButtonCol
from sqlalchemy import types
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import _pickle as pickle
import uuid
import random
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    current_list = db.Column(db.String(100))
    listdb = db.relationship('Listdb', backref='shopper', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    gym = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    restrictions = db.Column(db.String(10))
    cuisine = db.Column(db.String(200))
    complexity = db.Column(db.Integer)
    daily_cal = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    carb = db.Column(db.Integer)
    scores_fn = db.Column(db.String)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self,size):
        digest=md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://gravatar.com/avatar/{}?d=retro&s={}'.format(digest,size)

    def nutrigen(self):
        self.daily_cal = nutrition.calc_cal(self.weight, self.height, self.age, self.gender, self.gym, self.goals)
        self.protein, self.fat, self.carb = nutrition.calc_macros(self.daily_cal, self.weight, self.goals)

    def list_initialize(self):
        self.scores_fn = nutrition.list_gen()




class Listdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    list_name = db.Column(db.String(100))
    file_name = db.Column(db.String(300))

    def __repr__(self):
        return '<Listdb {}>'.format(self.list_name)

## If we were using Relational DB, may want to construct Grocery lists as db
class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Grocery {}>'.format(self.items)

class GroceryList:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.groc_list = [] # initialize with empty list of items
        self.filename = uuid.uuid4().hex + '.pkl'

    def add_item(self, item):
        self.groc_list.append(item)
        print(item + " has been added to " + self.name + ".")

    def delete_item(self, item):
        self.groc_list.remove(item)
        print(item + " has been removed from " + self.name + ".")

    def get_items(self):
        print("Current items in " + self.name + ":")
        for item in self.groc_list:
            print(item)

    def save_list(self):
        with open(self.filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(self, output, -1)

    def clear_list(self):
        self.groc_list = []

## Table for ingredients from search
class IngrTable(Table):
    name = Col('Ingredient')
    but_add = ButtonCol('+', 'add_food_item', url_kwargs = dict(food_item = 'name'))

## Table for active grocery list
class ListTable(Table):
    name = Col('Ingredient')
    but_add = ButtonCol('-', 'del_food_item', url_kwargs = dict(food_item = 'name'))

## Another for ingredients
class Ingr(object):
    def __init__(self, name, but_add):
        self.name = name
        self.but_add = but_add

## Table for all user's grocery lists
class GrocListTable(Table):
    name = Col('ListName')
    but_load = ButtonCol('Load', 'f_load_list', url_kwargs = dict(f_list = 'name'))
    but_del = ButtonCol('Delete', 'f_del_list', url_kwargs = dict(f_list = 'name'))

## Another for ingredients
class GrocListTableItem(object):
    def __init__(self, name, but_load, but_del):
        self.name = name
        self.but_load = but_load
        self.but_del = but_del

## Table for all user's grocery lists
class RecListTable(Table):
    name = Col('RecName')
    kcal = Col('Calories')
    fat = Col('Fat (g)')
    carb = Col('Carbohydrates (g)')
    protein = Col('Protein (g)')
    prods = Col('Ingredients to Add to List')
    nutScore = Col('Nutrition Match')
    user_score = Col('Preference Match')

## Another for ingredients
class RecListTableItem(object):
    def __init__(self, name, kcal, fat, carb, protein, prods, nutScore, user_score):
        self.name = name
        self.kcal = kcal
        self.fat = fat
        self.carb = carb
        self.protein = protein
        self.prods = prods
        self.nutScore = nutScore
        self.user_score = user_score  
