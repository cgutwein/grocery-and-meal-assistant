from prototype import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_table import Table, Col, ButtonCol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import _pickle as pickle
import uuid
import random

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

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

## Table for ingredients from search
class ListTable(Table):
    name = Col('Ingredient')
    but_add = ButtonCol('-', 'del_food_item', url_kwargs = dict(food_item = 'name'))

## Another for ingredients
class Ingr(object):
    def __init__(self, name, but_add):
        self.name = name
        self.but_add = but_add
