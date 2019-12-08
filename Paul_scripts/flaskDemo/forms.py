from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import DecimalField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, DecimalField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Algorithm, Gene, Job, KNN_Model, Population, Pred_Result, RF_Model, SVR_Model, User
from wtforms.fields.html5 import DateField
from wtforms.fields import Field
import sys


gene_names = Gene.query.with_entities(Gene.gene_name).distinct()
gene_name_choices = [(row[0], row[0]) for row in gene_names]

pop_id = Population.query.with_entities(Population.population_id).distinct()
pop = [(row[0], row[0]) for row in pop_id]

class Add_Gene_Model(FlaskForm):
    genename = SelectField("Gene Name", choices=gene_name_choices,
                           validators=[InputRequired()]) #I used gene name to make it easier for
    #users to be able to search genes. Then with gene name, I can get the gene_id and add that to
    #the model table
    pop_id = SelectField("Population ID", choices=pop,
                         validators=[InputRequired()])
    cross_val = DecimalField("Cross Validation Value",
                             validators=[InputRequired()])

class KNN(Add_Gene_Model):
    neigbor = IntegerField("Neigbour", validators=[DataRequired()])
    weight = StringField("Weight", validators=[DataRequired(), Length(min=5, max=20)])
    p = IntegerField("P", validators=[DataRequired()])
    submit = SubmitField("Add Gene Model")

    def validate_genename(self, genename):
        gene = Gene.query.filter_by(gene_name=genename.data).first()
        knndb = KNN_Model.query.filter_by(gene_id=gene.gene_id).first()
        if knndb and (str(knndb.population_id) == str(self.pop_id.data)):
            raise ValidationError("There is a model for that gene and population")

class RF(Add_Gene_Model):
    tree = IntegerField("Tree", validators=[DataRequired()])
    submit = SubmitField("Add Gene Model")
    
    def validate_genename(self, genename):
        gene = Gene.query.filter_by(gene_name=genename.data).first()
        rfdb = RF_Model.query.filter_by(gene_id=gene.gene_id).first()
        if rfdb and (str(rfdb.population_id) == str(self.pop_id.data)):
            raise ValidationError("There is a model for that gene and population")


class SVR(Add_Gene_Model):
    kernel = StringField("Kernel", validators=[DataRequired(), Length(min=1, max=20)])
    degree = IntegerField("Degree", validators=[DataRequired()])
    c = DecimalField("C", validators=[DataRequired()])
    submit = SubmitField("Add Gene Model")

    def validate_genename(self, genename):
        gene = Gene.query.filter_by(gene_name=genename.data).first()
        svrdb = SVR_Model.query.filter_by(gene_id=gene.gene_id).first()
        if svrdb and (str(svrdb.population_id) == str(self.pop_id.data)):
            raise ValidationError("There is a model for that gene and population")

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

