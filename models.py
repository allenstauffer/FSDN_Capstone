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
class Movies(db.Model):  
  __tablename__ = 'Movies'

  movies_id = Column('movies_id',Integer, primary_key=True)
  movies_title = Column('movies_title',String)
  movies_release_date = db.Column('movies_release_date', db.DateTime)

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
class Actors(db.Model):  
  __tablename__ = 'Actors'

  actors_id = Column('actors_id',Integer, primary_key=True)
  actors_name = Column('actors_name', String)
  actors_age = Column('actors_age', Integer)
  actors_gender = Column('actors_gender', String)

  def __init__(self, actors_name="", actors_age=0, actors_gender=""):
    self.actors_name = actors_name
    self.actors_age = actors_age
    self.actors_gender = actors_gender

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
      'actors_name': self.actors_name,
      'actors_age': self.actors_age,
      'actors_gender': self.actors_gender}