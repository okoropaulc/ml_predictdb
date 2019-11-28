from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##class User(db.Model, UserMixin):
##    __table_args__ = {'extend_existing': True}
##    id = db.Column(db.Integer, primary_key=True)
##    username = db.Column(db.String(20), unique=True, nullable=False)
##    email = db.Column(db.String(120), unique=True, nullable=False)
##    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
##    password = db.Column(db.String(60), nullable=False)
##
##    def __repr__(self):
##        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class User(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['user']
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

  
