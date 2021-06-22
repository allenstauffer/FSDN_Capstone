import os
from flask import Flask
from models import setup_db
from flask_cors import CORS
from models import Movies, Actors


def get_actors():
    actors = Actors.query.all()
    if len(actors) == 0:
        abort(404)
    return actors

def get_movies():
    movies = Movies.query.all()
    if len(movies) == 0:
        abort(404)
    return movies


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors', methods=['GET'])
    def get_drinks():
        return jsonify({
            'success': True,
            'actors': get_actors()
        })

    @app.route('/movies', methods=['GET'])
    def get_drinks():
        return jsonify({
            'success': True,
            'movies': get_movies()
        })


    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    # @app.route('/coolkids')
    # def be_cool():
    #     return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()