import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, GeneModelForm
from flaskDemo.models import Algorithm, Gene, Population, GeneModel, User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        form = GeneModelForm()
        if form.validate_on_submit():
            exists = GeneModel.query.filter_by(geneID=form.gene.data, popID=form.pop.data, algoID=form.algo.data).first()
            crossval = str(exists.cross_val)
            return render_template('query_genome_database.html', title='Query Genome Database',
                               form=form, crossval=crossval, legend='Query Genome Database')
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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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

@app.route("/assign/", methods=['GET', 'POST'])
@login_required
def assign_intro():
    form = AssignForm()
    if form.validate_on_submit():
        works_on_exists = Works_On.query.filter_by(essn=form.ssn.data, pno=form.pno.data).first()
        
        if works_on_exists:
            works_on_exists.hours = form.hours.data
            db.session.commit()
            flash('You have updated an assignment!', 'success')
            return redirect(url_for('assign', pno=form.pno.data, essn=form.ssn.data))
        else:
            works_on = Works_On(essn=form.ssn.data, pno=form.pno.data, hours=form.hours.data)
            db.session.add(works_on)
            db.session.commit()
            flash('You have added a new assignment!', 'success')
            return redirect(url_for('home'))
    return render_template('assign_add_or_update.html', title='Add/Update Assignment',
                           form=form, legend='Add/Update Assignment')

@app.route("/assign/<pno>/<essn>")
@login_required
def assign(pno, essn):
    assign = Works_On.query.get_or_404([essn,pno])
    return render_template('assign.html', title=str(assign.essn) + "_" + str(assign.pno), assign=assign, now=datetime.utcnow())

@app.route("/assign/<pno>/<essn>/delete", methods=['POST'])
@login_required
def delete_assign(pno, essn):
    assign = Works_On.query.get_or_404([essn,pno])
    db.session.delete(assign)
    db.session.commit()
    flash('The assignment has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/assign/<pno>/<essn>/update", methods=['GET', 'POST'])
@login_required
def update_assign(pno, essn):
    assign = Works_On.query.get_or_404([essn,pno])

    form = AssignForm()

    if form.validate_on_submit():
        works_on_exists = Works_On.query.filter_by(essn=form.ssn.data, pno=form.pno.data).first()
        if works_on_exists:
            works_on_exists.hours = form.hours.data
            db.session.commit()
            flash('You have updated an assignment!', 'success')
            return redirect(url_for('assign', pno=form.pno.data, essn=form.ssn.data))
        else:
            works_on = Works_On(essn=form.ssn.data, pno=form.pno.data, hours=form.hours.data)
            db.session.add(works_on)
            db.session.commit()
            flash('You have added a new assignment!', 'success')
            return redirect(url_for('home'))
    elif request.method == 'GET':             
        form.ssn.data = assign.essn  
        form.pno.data = assign.pno
        form.hours.data = assign.hours
    return render_template('assign_add_or_update.html', title='Update Assignment',
                           form=form, legend='Update Assignment') 
