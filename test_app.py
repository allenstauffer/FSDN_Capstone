import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import datetime
from app import create_app
from models import setup_db, Movie, Actor


class Capstone(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_NAME = 'capstone_test'
        self.database_path = "postgresql://{}@{}/{}".format(self.DB_USER,
                                                            self.DB_HOST,
                                                            self.DB_NAME)
        self.bad_token = "{}{}{}{}".format("00000000000000000000000000",
                                           "00000000000000000000000000",
                                           "00000000000000000000000000",
                                           "00000000000000000000000000",
                                           "0000000000000000000000")
        self.token_casting_assistant = os.getenv('TOKEN_CASTING_ASSISTANT')
        self.token_casting_director = os.getenv('TOKEN_CASTING_DIRECTOR')
        self.token_executive_producer = os.getenv('TOKEN_EXECUTIVE_PRODUCER')
        self.del_time = 'Sat, 23 May 2026 00:00:00 GMT'
        self.newDate = datetime.date(2026, 5, 23)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.db.session.query(Actor).delete()
            self.db.session.query(Movie).delete()
            self.new_actor = {"name": "new actor",
                              "age": 34,
                              "gender": "male"}
            self.new_actor_executive_producer = {"name": "exec",
                                                 "age": 36,
                                                 "gender": "female"}
            self.new_movie = {"title": "new movie",
                              "release_date": self.newDate}
            self.new_movie_executive_producer = {"title": "new movie producer",
                                                 "release_date": self.newDate}
            self.delete_actor = Actor(actor_name="deleted actor",
                                      actor_age=39,
                                      actor_gender="female")
            self.delete_actor_producer = Actor(actor_name="delete prod actor",
                                               actor_age=21,
                                               actor_gender="male")
            self.add_actor = Actor(actor_name="additional actor",
                                   actor_age=21,
                                   actor_gender="male")
            self.add_actor2 = Actor(actor_name="additional 2 actor",
                                    actor_age=32,
                                    actor_gender="female")
            self.delete_movie = Movie(movie_title="deleted movie",
                                      movie_release_date=self.newDate)
            self.delete_movie_prod = Movie(movie_title="deleted movie prod",
                                           movie_release_date=self.del_time)
            self.add_movie = Movie(movie_title="additional movie",
                                   movie_release_date=self.newDate)
            self.add_movie2 = Movie(movie_title="additional 2 movie",
                                    movie_release_date=self.newDate)
            self.add_movie3 = Movie(movie_title="additional 3 movie",
                                    movie_release_date=self.newDate)
            self.db.session.add(self.delete_actor)
            self.db.session.add(self.delete_actor_producer)
            self.db.session.add(self.add_actor)
            self.db.session.add(self.add_actor2)
            self.db.session.add(self.delete_movie)
            self.db.session.add(self.delete_movie_prod)
            self.db.session.add(self.add_movie)
            self.db.session.add(self.add_movie2)
            self.db.session.commit()
            self.delete_actor_id = self.delete_actor.id
            self.delete_actor_producer_id = self.delete_actor_producer.id
            self.delete_movie_id = self.delete_movie.id
            self.delete_movie_prod_id = self.delete_movie_prod.id
            self.total_actors = 4
            self.total_movies = 5

    def tearDown(self):
        """Executed after reach test"""
        pass

    def send_token_request_get(self, path, token):
        return self.client().get(path, headers={
            "Authorization": 'bearer {}'.format(token)
        })

    def send_token_request_post(self, path, token, json):
        return self.client().post(path, headers={
            "Authorization": 'bearer {}'.format(token)
        }, json=json)

    def send_token_request_put(self, path, token, json):
        return self.client().put(path, headers={
            "Authorization": 'bearer {}'.format(token)
        }, json=json)

    def send_token_request_delete(self, path, token):
        return self.client().delete(path, headers={
            "Authorization": 'bearer {}'.format(token)
        })

    # #Actor Tests
    def test_get_actors_noheader(self):
        self.assertTrue(True)
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_actors_noheader_specific(self):
        self.assertTrue(True)
        res = self.client().get('/actors/10')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_actors_casting_assistant(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_get(path, self.token_casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']["id"],
                         self.delete_actor_id)
        self.assertEqual(data['actor']["actor_name"],
                         self.delete_actor.actor_name)
        self.assertEqual(data['actor']["actor_age"],
                         self.delete_actor.actor_age)
        self.assertEqual(data['actor']["actor_gender"],
                         self.delete_actor.actor_gender)

    def test_get_actors_casting_director(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_get(path, self.token_casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']["id"],
                         self.delete_actor_id)
        self.assertEqual(data['actor']["actor_name"],
                         self.delete_actor.actor_name)
        self.assertEqual(data['actor']["actor_age"],
                         self.delete_actor.actor_age)
        self.assertEqual(data['actor']["actor_gender"],
                         self.delete_actor.actor_gender)

    def test_get_actors_executive_producer(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_get(path, self.token_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']["id"],
                         self.delete_actor_id)
        self.assertEqual(data['actor']["actor_name"],
                         self.delete_actor.actor_name)
        self.assertEqual(data['actor']["actor_age"],
                         self.delete_actor.actor_age)
        self.assertEqual(data['actor']["actor_gender"],
                         self.delete_actor.actor_gender)

    def test_get_actors_executive_producer_not_found(self):
        self.assertTrue(True)
        path = "/actors/-1"
        res = self.send_token_request_get(path, self.token_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actors_casting_assistant_all(self):
        self.assertTrue(True)
        path = "/actors"
        res = self.send_token_request_get(path, self.token_casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), self.total_actors)

    def test_get_actors_casting_director_all(self):
        self.assertTrue(True)
        path = "/actors"
        res = self.send_token_request_get(path, self.token_casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), self.total_actors)

    def test_get_actors_executive_producer_all(self):
        self.assertTrue(True)
        path = "/actors"
        res = self.send_token_request_get(path, self.token_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), self.total_actors)

    def test_post_actors_casting_assistant(self):
        self.assertTrue(True)
        path = "/actors"
        res = self.send_token_request_post(path,
                                           self.token_casting_assistant,
                                           self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_post_actors_casting_director(self):
        self.assertTrue(True)
        newCount = len(Actor.query.all()) + 1
        path = "/actors"
        res = self.send_token_request_post(path,
                                           self.token_casting_director,
                                           self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(Actor.query.all()), newCount)

    def test_post_actors_executive_producer(self):
        self.assertTrue(True)
        newCount = len(Actor.query.all()) + 1
        path = "/actors"
        res = self.send_token_request_post(path,
                                           self.token_executive_producer,
                                           self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(Actor.query.all()), newCount)

    def test_post_actors_executive_producer_malformedName(self):
        self.assertTrue(True)
        path = "/actors"
        res = self.send_token_request_post(path,
                                           self.token_executive_producer,
                                           {"age": 0, "gender": "female"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_post_actors_executive_producer_malformedAge(self):
        self.assertTrue(True)
        path = "/actors"
        res = self.send_token_request_post(path,
                                           self.token_executive_producer,
                                           {"name": "test",
                                            "gender": "female"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_post_actors_executive_producer_malformedGender(self):
        self.assertTrue(True)
        path = "/actors"
        res = self.send_token_request_post(path,
                                           self.token_executive_producer,
                                           {"name": "test", "age": 0})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_put_actors_casting_assistant(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_put(path,
                                          self.token_casting_assistant,
                                          self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'],
                        "Authorization header is expected.")

    def test_put_actors_casting_assistant(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_put(path,
                                          self.token_casting_director,
                                          self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_put_actors_executive_producer(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_producer_id)
        res = self.send_token_request_put(path,
                                          self.token_executive_producer,
                                          self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_put_actors_executive_producer_notfound(self):
        self.assertTrue(True)
        path = "/actors/-1"
        res = self.send_token_request_put(path,
                                          self.token_executive_producer,
                                          {"age": 0, "gender": "female"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_put_actors_executive_producer_malformedName(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_put(path,
                                          self.token_executive_producer,
                                          {"age": 0, "gender": "female"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_put_actors_executive_producer_malformedAge(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_put(path,
                                          self.token_executive_producer,
                                          {"name": "test", "gender": "female"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_put_actors_executive_producer_malformedGender(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_put(path,
                                          self.token_executive_producer,
                                          {"name": "test", "age": 0})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_delete_actors_casting_assistant(self):
        self.assertTrue(True)
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_delete(path,
                                             self.token_casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actors_casting_director(self):
        self.assertTrue(True)
        newCount = len(Actor.query.all()) - 1
        path = "/actors/{}".format(self.delete_actor_id)
        res = self.send_token_request_delete(path,
                                             self.token_casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(Actor.query.all()), newCount)
        self.assertEqual(Actor.query.get(self.delete_actor_id), None)

    def test_delete_actors_executive_producer(self):
        self.assertTrue(True)
        newCount = len(Actor.query.all()) - 1
        path = "/actors/{}".format(self.delete_actor_producer_id)
        res = self.send_token_request_delete(path,
                                             self.token_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(Actor.query.all()), newCount)
        self.assertEqual(Actor.query.get(self.delete_actor_producer_id), None)

    # Movie Tests
    def test_get_movies_noheader(self):
        self.assertTrue(True)
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_movies_noheader_specific(self):
        self.assertTrue(True)
        res = self.client().get('/movies/10')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_movies_casting_assistant(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_id)
        res = self.send_token_request_get(path, self.token_casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']["id"],
                         self.delete_movie_id)
        self.assertEqual(data['movie']["movie_title"],
                         self.delete_movie.movie_title)
        self.assertEqual(data['movie']["movie_release_date"],
                         self.del_time)

    def test_get_movies_casting_director(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_id)
        res = self.send_token_request_get(path,
                                          self.token_casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']["id"], self.delete_movie_id)
        self.assertEqual(data['movie']["movie_title"],
                         self.delete_movie.movie_title)
        self.assertEqual(data['movie']["movie_release_date"],
                         self.del_time)

    def test_get_movies_executive_producer(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_prod_id)
        res = self.send_token_request_get(path,
                                          self.token_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']["id"],
                         self.delete_movie_prod_id)
        self.assertEqual(data['movie']["movie_title"],
                         self.delete_movie_prod.movie_title)
        self.assertEqual(data['movie']["movie_release_date"],
                         self.del_time)

    def test_get_movies_executive_producer_not_found(self):
        self.assertTrue(True)
        path = "/movies/-1"
        res = self.send_token_request_get(path,
                                          self.token_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies_casting_assistant_all(self):
        self.assertTrue(True)
        path = "/movies"
        res = self.send_token_request_get(path, self.token_casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), self.total_actors)

    def test_get_movies_casting_director_all(self):
        self.assertTrue(True)
        path = "/movies"
        res = self.send_token_request_get(path, self.token_casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), self.total_actors)

    def test_get_movies_executive_producer_all(self):
        self.assertTrue(True)
        path = "/movies"
        res = self.send_token_request_get(path,
                                          self.token_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), self.total_actors)

    def test_post_movies_casting_assistant(self):
        self.assertTrue(True)
        path = "/movies"
        res = self.send_token_request_post(path,
                                           self.token_casting_assistant,
                                           self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_post_movies_casting_director(self):
        self.assertTrue(True)
        newCount = len(Actor.query.all()) + 1
        path = "/movies"
        res = self.send_token_request_post(path,
                                           self.token_casting_director,
                                           self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_post_movies_executive_producer(self):
        self.assertTrue(True)
        newCount = len(Movie.query.all()) + 1
        path = "/movies"
        res = self.send_token_request_post(path,
                                           self.token_executive_producer,
                                           self.new_movie_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(Movie.query.all()), newCount)

    def test_post_movies_executive_producer_malformedTitle(self):
        self.assertTrue(True)
        path = "/movies"
        res = self.send_token_request_post(path,
                                           self.token_executive_producer,
                                           {"title": "test"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_post_movies_executive_producer_malformedReleasedDate(self):
        self.assertTrue(True)
        path = "/movies"
        res = self.send_token_request_post(path,
                                           self.token_executive_producer,
                                           {"release_date":
                                            datetime.date(2026, 5, 23)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_put_movies_casting_assistant(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_id)
        res = self.send_token_request_put(path,
                                          self.token_casting_assistant,
                                          self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_put_movies_casting_assistant(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_id)
        res = self.send_token_request_put(path,
                                          self.token_casting_director,
                                          self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_put_movies_executive_producer(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_prod_id)
        res = self.send_token_request_put(path,
                                          self.token_executive_producer,
                                          self.new_movie_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_put_movies_executive_producer_notfound(self):
        self.assertTrue(True)
        path = "/movies/-1"
        res = self.send_token_request_put(path,
                                          self.token_executive_producer,
                                          self.new_movie_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_put_movies_executive_producer_malformedTitle(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_prod_id)
        res = self.send_token_request_put(path,
                                          self.token_executive_producer,
                                          {"title": "test"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_put_movies_executive_producer_malformedReleasedDate(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_prod_id)
        res = self.send_token_request_put(path,
                                          self.token_executive_producer,
                                          {"release_date":
                                           datetime.date(2026, 5, 23)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_delete_movies_casting_assistant(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_id)
        res = self.send_token_request_delete(path,
                                             self.token_casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_delete_movies_casting_director(self):
        self.assertTrue(True)
        path = "/movies/{}".format(self.delete_movie_id)
        res = self.send_token_request_delete(path,
                                             self.token_casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_delete_movies_executive_producer(self):
        self.assertTrue(True)
        newCount = len(Movie.query.all()) - 1
        path = "/movies/{}".format(self.delete_movie_prod_id)
        res = self.send_token_request_delete(path,
                                             self.token_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(Movie.query.all()), newCount)
        self.assertEqual(Actor.query.get(self.delete_movie_prod_id), None)

    def test_delete_movies_executive_producer_notFound(self):
        self.assertTrue(True)
        path = "/movies/-1"
        res = self.send_token_request_delete(path,
                                             self.token_executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
