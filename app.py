import os
from flask import Flask, request, jsonify, abort
from models import setup_db
from flask_cors import CORS
from models import Movie, Actor
import sys
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, id):
        actor = Actor.query.get(id)
        if actor == None:
            abort(404)
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, id):
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)            
        actor.delete()
        return jsonify({
            "success": True,
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        body = request.get_json()
        actor_name = body.get('name', None)
        actor_age = body.get('age', None)
        actor_gender = body.get('gender', None)
        if actor_name is None or actor_age is None or actor_gender is None:
            abort(400)
        actor = Actor(
            actor_name=actor_name,
            actor_age=actor_age,
            actor_gender=actor_gender
        )
        actor.insert()
        return jsonify({
            "success": True,
        }), 200
    
    @app.route('/actors/<int:id>', methods=['PUT'])
    @requires_auth('put:actors')
    def put_actors(payload, id):
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)                 
        body = request.get_json()
        actor_name = body.get('name', None)
        actor_age = body.get('age', None)
        actor_gender = body.get('gender', None)
        if actor_name is None or actor_age is None or actor_gender is None:
            abort(400)
        actor.actor_name=actor_name
        actor.actor_age=actor_age
        actor.actor_gender=actor_gender
        actor.update()
        return jsonify({
            "success": True,
        }), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        if len(movies) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, id):
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)            
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, id):
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)            
        movie.delete()
        return jsonify({
            "success": True,
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        if title is None or release_date is None:
            abort(400)
        movie = Movie(
            movie_title=title,
            movie_release_date=release_date
        )
        movie.insert()
        return jsonify({
            'success': True,
        }), 200

    @app.route('/movies/<int:id>', methods=['PUT'])
    @requires_auth('put:movies')
    def put_movies(payload, id):
        body = request.get_json()
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)            
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        if title is None or release_date is None:
            abort(400)
        movie.movie_title=title
        movie.movie_release_date=release_date
        movie.update()
        return jsonify({
            'success': True,
        }), 200

    # Error Handling
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

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
            }), 401

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
            }), AuthError.status_code


    return app

app = create_app()

if __name__ == '__main__':
    app.run()