from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, RadioField, SelectMultipleField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
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
    userage = IntegerField('Enter your age (years)', default=30, validators=[DataRequired()])
    userheight = IntegerField('Enter your height (in)', default=65 , validators=[DataRequired()])
    userweight = IntegerField('Enter your weight (lbs)', default=140, validators=[DataRequired()])
    usergender = RadioField('Enter your gender', default='f', choices=[('m', 'Male'), ('f', 'Female')], validators=[DataRequired()])
    usergym = RadioField('How often do you exercise?', default='l', choices=[('l', 'Less than twice a week'), ('m', 'Less than four times a week'), ('h', 'Four or more times a week')], validators=[DataRequired()])
    usergoals = RadioField('What are your nutritional goals?', default='l', choices=[('l', 'Weight loss'), ('g', 'Mass gain'), ('n', 'Already perfect')], validators=[DataRequired()])
    userspecs = RadioField('Do you have dietary restrictions?', default='ve', choices=[('ve', 'Vegan'), ('vg', 'Vegetarian'), ('n', 'None')], validators=[DataRequired()])
    usercuisine = SelectMultipleField('Select your preferred cuisine(s)?', default='all', choices=[('all', 'ALL'),('mex', 'mexican'),('fre', 'french'),('iri', 'irish'),('ita', 'italian'),('chi', 'chinese'),('sus', 'southern_us'),('tha', 'thai'),('kor', 'korean'),('mor', 'moroccan'),('spa', 'spanish'),('gre', 'greek'),('bri', 'british'),('ind', 'indian'),('vie', 'vietnamese'),('jam', 'jamaican'),('jap', 'japanese'),('caj', 'cajun_creole'),('rus', 'russian'),('bra', 'brazilian'),('fil', 'filipino')], validators=[DataRequired()])
    usercomplex = RadioField('Select preferred cooking complexity', default='l', choices=[('l', 'Low'), ('m', 'Medium'), ('h', 'High')], validators=[DataRequired()])
    usermeal = RadioField('Select the meal of the day', default='b', choices=[('b', 'Breakfast'), ('l', 'Lunch'), ('d', 'dinner')], validators=[DataRequired()])
    userrecipe = FileField('Upload Recipe', validators=[DataRequired()])
    submit = SubmitField('Give me recipes!!!')