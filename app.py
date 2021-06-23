import os
from flask import Flask, request, jsonify, abort
from models import setup_db
from flask_cors import CORS
from models import Movie, Actor
import sys

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actors.query.all()
        if len(actors) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': actors
        })

    @app.route('/actors', methods=['POST'])
    def post_actors():
        try:
            body = request.get_json()
            actor_name = body.get('name', None)
            actor_age = body.get('age', None)
            actor_gender = body.get('gender', None)

            print("actor_name")
            print(actor_name)
            print("actor_age")
            print(actor_age)
            print("actor_gender")
            print(actor_gender)
            if actor_name is None or actor_age is None or actor_gender is None:
                abort(401)
            print("here")
            actor = Actor(
                actor_name=actor_name,
                actor_age=actor_age,
                actor_gender=actor_gender
            )
            print("here again")
            actor.insert()
            return jsonify({
                "success": True,
            }), 200
        except Exception:
            print(sys.exc_info())
            abort(422)  

    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movies.query.all()
        if len(movies) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': movies()
        })

    @app.route('/movies', methods=['POST'])
    def post_movies():
        try:
            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release_date', None)
            if title is None or release_date is None:
                abort(401)
            movie = Movie(
                title=title,
                recipe=release_date
            )
            drink.insert()
            returnArray = [drink.long()]
            return jsonify({
                'success': True,
                'drinks': returnArray
            })
        except Exception:
            print(sys.exc_info())
            abort(422)  



    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"


    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
            }), 400


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404


    # @app.errorhandler(AuthError)
    # def authentification_failed(AuthError):
    #     return jsonify({
    #         "success": False,
    #         "error": AuthError.status_code,
    #         "message": AuthError.error['description']
    #         }), AuthError.status_code


    return app

app = create_app()

if __name__ == '__main__':
    app.run()