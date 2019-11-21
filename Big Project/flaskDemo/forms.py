from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Gene, Population, Algorithm, GeneModel
from wtforms.fields.html5 import DateField

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class GeneModelForm(FlaskForm):
    genes = Gene.query.with_entities(Gene.ID, Gene.chromono, Gene.name, Gene.type).order_by(Gene.name)
    algorithms = Algorithm.query.with_entities(Algorithm.ID, Algorithm.description).order_by(Algorithm.description)
    populations = Population.query.with_entities(Population.ID, Population.description).order_by(Population.description)

    genechoices = [(row[0],row[2] + " (" + str(row[3]) + ")") for row in genes]
    algochoices = [(row[0],row[1]) for row in algorithms]
    popchoices = [(row[0],row[1]) for row in populations]

    gene = SelectField("Gene", choices=genechoices)  
    algo = SelectField("Algorithm", choices=algochoices)
    pop = SelectField("Population", choices=popchoices)
    submit = SubmitField('Get Cross_Val Performance')

    def validate_gene(form, field):    
        validated = GeneModel.query.filter_by(geneID=form.gene.data, popID=form.pop.data, algoID=form.algo.data).first()
        if validated is None:
            raise ValidationError('That combination of gene, population, and algorithm is not yet in the database.')
