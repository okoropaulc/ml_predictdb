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
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    user_type = SelectField('Choose User Type',
                            choices=[('Admin', 'Admin'),('Regular','Regular')],
                            validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

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

