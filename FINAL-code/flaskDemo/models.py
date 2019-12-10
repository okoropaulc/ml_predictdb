from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
#from functools import partial
#from sqlalchemy import orm
db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['user']
    def get_id(self):
        return (self.user_id) #i added this so as to overide get_id which forces me to name a column in user table 'id'
class Algorithm(db.Model):
    __table__ = db.Model.metadata.tables['algorithm']
class Gene(db.Model):
    __table__ = db.Model.metadata.tables['gene']
class Population(db.Model):
    __table__ = db.Model.metadata.tables['population']
class KNN_Model(db.Model):
    __table__ = db.Model.metadata.tables['knn_model']
class RF_Model(db.Model):
    __table__ = db.Model.metadata.tables['rf_model']
class SVR_Model(db.Model):
    __table__ = db.Model.metadata.tables['svr_model']
class Job(db.Model):
    __table__ = db.Model.metadata.tables['job']
class Pred_Result(db.Model):
    __table__ = db.Model.metadata.tables['prediction_result']


















"""
class Algorithm(db.Model):
    __tablename__ = 'algorithm'
    algorithm_id = db.Column(db.String, primary_key=True)
    algorithm_description = db.Column(db.String)

class Gene(db.Model):
    __tablename__ = 'gene'
    gene_id = db.Column(db.String, primary_key=True)
    gene_name = db.Column(db.String)
    gene_type = db.Column(db.String)
    chromosome_no = db.Column(db.Integer)

class Job(db.Model):
    __tablename__ = 'job'
    job_id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String)
    job_description = db.Column(db.String)
    job_status = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

class Knn_Model(db.Model):
    __tablename__ = 'knn_model'
    gene_id = db.Column(db.String, db.ForeignKey('gene.gene_id'))
    population_id = db.Column(db.String, db.ForeignKey('population.population_id'))
    cross_val_performance = db.Column(db.Float)
    neighbors = db.Column(db.Integer)
    weight = db.Column(db.String)
    p = db.Column(db.Integer)

class Population(db.Model):
    __tablename__ = 'population'
    population_id = db.Column(db.String, primary_key=True)
    population_description = db.Column(db.String)

class Prediction_Result(db.Model):
    __tablename__ = 'prediction_result'
    gene_id = db.Column(db.String, db.ForeignKey('gene.gene_id'))
    algorithm_id = db.Column(db.String, db.ForeignKey('algorithm.algorithm_id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'))
    population_id = db.Column(db.String, db.ForeignKey('population.population_id'))
    predicted_value = db.Column(db.Float)

class Rf_Model(db.Model):
    __tablename__ = 'rf_model'
    gene_id = db.Column(db.String, db.ForeignKey('gene.gene_id'))
    population_id = db.Column(db.String, db.ForeignKey('population.population_id'))
    cross_val_performance = db.Column(db.Float)
    trees = db.Column(db.Integer)

class Svr_Model(db.Model):
    __tablename__ = 'svr_model'
    gene_id = db.Column(db.String, db.ForeignKey('gene.gene_id'))
    population_id = db.Column(db.String, db.ForeignKey('population.population_id'))
    cross_val_performance = db.Column(db.Float)
    kernel = db.Column(db.String)
    degree = db.Column(db.Integer)
    c = db.Column(db.Float)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)
    user_type = db.Column(db.String)
"""

