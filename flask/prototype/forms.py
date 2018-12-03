from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, RadioField, SelectMultipleField, FileField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from prototype.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PreferencesForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    userage = IntegerField('Enter your age (years)', default=30, validators=[DataRequired()])
    userheight = IntegerField('Enter your height (in)', default=65 , validators=[DataRequired()])
    userweight = IntegerField('Enter your weight (lbs)', default=140, validators=[DataRequired()])
    usergender = RadioField('Enter your gender', default='f', choices=[('m', 'Male'), ('f', 'Female')], validators=[DataRequired()])
    usergym = RadioField('How often do you exercise?', default='0', choices=[('0', 'Never'),('1', 'Less than twice a week'), ('2', 'Less than four times a week'), ('3', 'Four or more times a week')], validators=[DataRequired()])
    usergoals = RadioField('What are your nutritional goals?', default='0', choices=[('0', 'Weight loss'), ('1', 'Mass gain'), ('2', 'Already perfect')], validators=[DataRequired()])
    userspecs = RadioField('Do you have dietary restrictions?', default='ve', choices=[('ve', 'Vegan'), ('vg', 'Vegetarian'), ('n', 'None')], validators=[DataRequired()])
    usercuisine = SelectMultipleField('Select your preferred cuisine(s)?', default='all', choices=[('all', 'ALL'),('mexican', 'mexican'),('french', 'french'),('italian', 'italian'),('chinese', 'chinese'),('southern_us', 'southern_us'),('thai', 'thai'),('moroccan', 'moroccan'),('spanish', 'spanish'),('greek', 'greek'),('indian', 'indian'),('japanese', 'japanese')], validators=[DataRequired()])
    usercomplex = RadioField('Select preferred cooking complexity', default='1', choices=[('0', 'Low'), ('1', 'Medium'), ('2', 'High')], validators=[DataRequired()])
    userrecipe = FileField('Upload Recipe')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit changes.')

class GroceryListForm(FlaskForm):
    load = SubmitField('Load Grocery List')
    new_name = StringField('e.g. my list', validators=[DataRequired()])
    new_submit = SubmitField('Create New List')

class GrocerySearchForm(FlaskForm):
    query = StringField('Search groceries...', validators=[DataRequired()])
    submit = SubmitField('Go!')

class RecipeGenForm(FlaskForm):
    meal_type = RadioField('What type of meal are you looking for?', default='dinner', choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('dessert', 'Dessert'), ('drink', 'Drink'), ('snack', 'Snack')], validators=[DataRequired()])
    dof = IntegerField('How many allowable subsitutions?', default=3, validators=[DataRequired()])
    sorting_field = RadioField('Sort by', default='title', choices=[('title', 'RecName'), ('calories', 'Calories'), ('fats', 'Fat (g)'), ('carbs', 'Carbohydrates (g)'), ('protein', 'Protein (g)'), ('products to add', 'Ingredients to Add to List'), ('nutrition penalty', 'Nutrition Match'), ('user score', 'Preference Match')], validators=[DataRequired()])
    submit = SubmitField('Give me recipes!')