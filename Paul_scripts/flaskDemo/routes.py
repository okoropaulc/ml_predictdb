import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import Add_Gene_Model, KNN, RF, SVR, RegistrationForm, LoginForm, GeneModelForm
from flaskDemo.models import Algorithm, Gene, Job, KNN_Model, Population, Pred_Result, RF_Model, SVR_Model, User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import sys

"""
@app.route("/")
@app.route("/home")
def home():
    genes = Gene.query.all()
    return render_template('all_gene.html', outString = genes)

"""
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    genes = Gene.query.all()
    if current_user.is_authenticated:
        form = GeneModelForm()
        if form.validate_on_submit():
            results = None
            results2 = None
            if form.algo.data=="KNN":
                for pop in form.pop.data:
                    for gene in form.gene.data:
                        results2 = Gene.query.join(KNN_Model, Gene.gene_id == KNN_Model.gene_id) \
                           .add_columns(Gene.gene_id, Gene.gene_name, Gene.gene_type, Gene.chromosome_no) \
                           .join(Population, Population.population_id == KNN_Model.population_id) \
                           .add_columns(Population.population_id, Population.population_description, KNN_Model.cross_val_performance, KNN_Model.neighbors, KNN_Model.weight, KNN_Model.p) \
                           .filter(Gene.gene_id==gene, Population.population_id==pop)
                        if results2 != None:
                            if results != None:
                                results = results.union(results2)
                            else:
                                results = results2
                algo = "K Nearest Neighbor"
            elif form.algo.data=="RF":
                for pop in form.pop.data:
                    for gene in form.gene.data:                      
                        results2 = Gene.query.join(RF_Model, Gene.gene_id == RF_Model.gene_id) \
                           .add_columns(Gene.gene_id, Gene.gene_name, Gene.gene_type, Gene.chromosome_no) \
                           .join(Population, Population.population_id == RF_Model.population_id) \
                           .add_columns(Population.population_id, Population.population_description, RF_Model.cross_val_performance, RF_Model.trees) \
                           .filter(Gene.gene_id==gene, Population.population_id==pop)
                        if results2 != None:
                            if results != None:
                                results = results.union(results2)
                            else:
                                results = results2
                algo = "Random Forest"
            elif form.algo.data=="SVR":
                for pop in form.pop.data:
                    for gene in form.gene.data:
                        results2 = Gene.query.join(SVR_Model, Gene.gene_id == SVR_Model.gene_id) \
                           .add_columns(Gene.gene_id, Gene.gene_name, Gene.gene_type, Gene.chromosome_no) \
                           .join(Population, Population.population_id == SVR_Model.population_id) \
                           .add_columns(Population.population_id, Population.population_description, SVR_Model.cross_val_performance, SVR_Model.kernel, SVR_Model.degree, SVR_Model.c) \
                           .filter(Gene.gene_id==gene, Population.population_id==pop)
                        if results2 != None:
                            if results != None:
                                results = results.union(results2)
                            else:
                                results = results2
                algo = "Support Vector Regression"

            print(results, file=sys.stderr)
            print(algo, file=sys.stderr)

            return render_template('results.html', title='Results', results=results, algo=algo)
        return render_template('query_genome_database.html', title='Query Genome Database',
                               form=form, legend='Query Genome Database')
    return render_template('all_gene.html', outString = genes)



@app.route("/about")
def about():
    return ""


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.firstname.data, last_name=form.lastname.data, user_type=form.user_type.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

"""
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

"""

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.user_type == "Admin":
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin_home'))
            else:
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('regular_home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
"""        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

"""


@app.route("/admin_home")
def admin_home():
    if current_user.is_authenticated:
        return "Welcome to Admin Page"


@app.route("/regular_home")
def regular_home():
    if current_user.is_authenticated:
        return "Welcome to Regular Page"

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    return ""

@app.route("/knn_model", methods=['GET', 'POST'])
def knn_model():
    form = KNN()
    if form.validate_on_submit():
        gene = Gene.query.filter_by(gene_name=form.genename.data).first()
        knn = KNN_Model(gene_id=gene.gene_id, population_id=form.pop_id.data,
                        cross_val_performance=form.cross_val.data,
                        neighbors=form.neigbor.data, weight=form.weight.data,
                        p=form.p.data)
        db.session.add(knn)
        db.session.commit()
        flash("You have added the gene model")
        return redirect(url_for('home'))
    return render_template('knn_model.html', title='New KNN Gene Model',
                           form=form, legend='KNN Model')


@app.route("/rf_model", methods=['GET', 'POST'])
def rf_model():
    form = RF()
    if form.validate_on_submit():
        gene = Gene.query.filter_by(gene_name=form.genename.data).first()
        rf = RF_Model(gene_id=gene.gene_id, population_id=form.pop_id.data,
                        cross_val_performance=form.cross_val.data,
                        trees=form.tree.data)
        db.session.add(rf)
        db.session.commit()
        flash("You have added the gene model")
        return redirect(url_for('home'))
    return render_template('rf_model.html', title='New RF Gene Model',
                           form=form, legend='RF Model')


@app.route("/svr_model", methods=['GET', 'POST'])
def svr_model():
    form = SVR()
    if form.validate_on_submit():
        gene = Gene.query.filter_by(gene_name=form.genename.data).first()
        svr = SVR_Model(gene_id=gene.gene_id, population_id=form.pop_id.data,
                        cross_val_performance=form.cross_val.data,
                        kernel=form.kernel.data, degree=form.degree.data, c=form.c.data)
        db.session.add(svr)
        db.session.commit()
        flash("You have added the gene model")
        return redirect(url_for('home'))
    return render_template('svr_model.html', title='New SVR Gene Model',
                           form=form, legend='SVR Model')
