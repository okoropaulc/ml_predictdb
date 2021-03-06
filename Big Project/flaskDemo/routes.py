import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, GeneModelForm
from flaskDemo.models import Algorithm, Gene, Job, KNN_Model, Population, Pred_Result, RF_Model, SVR_Model, User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import sys

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
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
    return render_template('home_notlogged.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_id=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
