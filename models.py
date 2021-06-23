import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
DB_USER = os.getenv('DB_USER', 'postgres')  
DB_NAME = os.getenv('DB_NAME', 'capstone')  
defaultPath = "postgresql://{}@{}/{}".format(DB_USER, DB_HOST, DB_NAME) 
database_path = os.getenv('DATABASE_URL', defaultPath)  

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Movie
Have title and release year
'''
class Movie(db.Model):  
  __tablename__ = 'movie'

  id = Column(Integer, primary_key=True, autoincrement=True)
  movies_title = Column(String)
  movies_release_date = db.Column(db.Date)

  def __init__(self, movies_title="", movies_release_date=datetime.today()):
    self.movies_title = movies_title
    self.movies_release_date = movies_release_date

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def update(self):
      db.session.commit()    

  def format(self):
    return {
      'id': self.id,
      'movies_title': self.movies_title,
      'movies_release_date': self.movies_release_date}

'''
Movie
Have title and release year
'''
class Actor(db.Model):  
  __tablename__ = 'actor'

  id = Column(Integer, primary_key=True, autoincrement=True)
  actor_name = Column(String)
  actor_age = Column(Integer)
  actor_gender = Column(String)

  def __init__(self, actor_name="", actor_age=0, actor_gender=""):
    self.actor_name = actor_name
    self.actor_age = actor_age
    self.actor_gender = actor_gender

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def update(self):
      db.session.commit()    

def format(self):
  return {
    'id': self.id,
    'actor_name': self.actor_name,
    'actor_age': self.actor_age,
    'actor_gender': self.actor_gender}