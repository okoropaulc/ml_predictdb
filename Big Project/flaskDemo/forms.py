from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, DecimalField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Algorithm, Gene, Job, KNN_Model, Population, Pred_Result, RF_Model, SVR_Model, User
from wtforms.fields.html5 import DateField
from wtforms.fields import Field
import sys

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
        user = User.query.filter_by(user_id=username.data).first()
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
            user = User.query.filter_by(id=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            
class GeneModelForm(FlaskForm):
    genes = Gene.query.with_entities(Gene.gene_id, Gene.chromosome_no, Gene.gene_name, Gene.gene_type).order_by(Gene.gene_name)
    algorithms = Algorithm.query.with_entities(Algorithm.algorithm_id, Algorithm.algorithm_description).order_by(Algorithm.algorithm_description)
    populations = Population.query.with_entities(Population.population_id, Population.population_description).order_by(Population.population_description)

    genechoices = [(row[0], row[2]) for row in genes]
    algochoices = [(row[0],row[1]) for row in algorithms]
    popchoices = [(row[0],row[1]) for row in populations]

    gene = SelectMultipleField("Gene", choices=genechoices, validators=[InputRequired()])
    algo = SelectField("Algorithm", choices=algochoices, validators=[InputRequired()])
    pop = SelectMultipleField("Population", choices=popchoices, validators=[InputRequired()])
    submit = SubmitField("Get Results")

##    def validate_gene(form, field):
##        algoID = form.algo.data[0]
##        if algoID=="KNN":
##            validated = KNN_Model.query.filter_by(gene_id=form.gene.data, population_id=form.pop.data[0]).first()
##        elif algoID=="RF":
##            validated = RF_Model.query.filter_by(gene_id=form.gene.data, population_id=form.pop.data[0]).first()
##        else:            
##            validated = SVR_Model.query.filter_by(gene_id=form.gene.data, population_id=form.pop.data[0]).first()
##        print(form.gene.data, file=sys.stderr)
##        print(form.pop.data, file=sys.stderr)
##        print(form.algo.data, file=sys.stderr)
##        print(validated, file=sys.stderr)
##        if validated is None:
##            raise ValidationError('That combination of gene, population, and algorithm is not yet in the database.')
