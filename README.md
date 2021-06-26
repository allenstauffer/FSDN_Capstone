# Capstone casting directory API Backend
This is the final assignment for the FSDN course through udacity. I am doing this so that I can pass my udacity course and move on at work.

## Getting Started

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
Need to create a local database called capstone and one called capstone_test
-createdb capstone or CREATE DATABASE capstone(windows)
-createdb capstone_test or CREATE DATABASE capstone_test(windows)

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Pushing to server on heroku
### Setting up heroku remote
git remote add heroku https://git.heroku.com/allen-stauffer-fsdn-capstone.git
### Pushing Changes to heroku
git push heroku master
### Updating the database if any changes are made to the db
heroku run python manage.py db upgrade --app allen-stauffer-fsdn-capstone.git

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

## User Roles
There are 3 user roles that will allow access to different data
### Casting Assistant
Can view actors and movies

### Casting Director
Can view actors and movies
Add or delete an actor from the database
Modify actors or movies

### Executive Producer
Can view actors and movies
Add or delete an actor from the database
Modify actors or movies
Add or delete a movie from the database

## Endpoints 
-URL of the API
all endpoints can be accessed from the following url: https://allen-stauffer-fsdn-capstone.herokuapp.com/
### GET /actors
- General:
    - Returns a list of actors

``` {
    "actors": [
        {
            "actor_age": 0,
            "actor_gender": "female",
            "actor_name": "test actor",
            "id": 2
        },
        {
            "actor_age": 0,
            "actor_gender": "female",
            "actor_name": "test actor",
            "id": 1
        },
        {
            "actor_age": 0,
            "actor_gender": "female",
            "actor_name": "test actor",
            "id": 3
        },
        {
            "actor_age": 0,
            "actor_gender": "female",
            "actor_name": "test actor",
            "id": 4
        },
        {
            "actor_age": 0,
            "actor_gender": "female",
            "actor_name": "test actor",
            "id": 5
        },
        {
            "actor_age": 0,
            "actor_gender": "female",
            "actor_name": "test actor",
            "id": 6
        }
    ],
    "success": true
}
```

### GET /actors/{id}
- General:
    - Returns an actor object

``` 
{
    "actor": {
        "actor_age": 0,
        "actor_gender": "female",
        "actor_name": "test actor",
        "id": 1
    },
    "success": true
}
```

### DELETE /actor/{question_id}
- General:
    - Deletes the actor of the given ID if it exists. Returns success or failure

```
{
  "success": true
}
```

#### POST /actors
- General:
    - Creates a new acor using the submitted name, age, and gender. Returns the success value. 

```
{
  "success": true,
}
```

#### PUT /actors
- General:
    - updates an actor using the submitted name, age, and gender. Returns the success value. 

```
{
  "success": true,
}
```


#### GET /movies
- General:
    - Returns a list of movies

``` {
    "movies": [
        {
            "id": 2,
            "movie_release_date": "Wed, 23 May 2012 00:00:00 GMT",
            "movie_title": "changed movie2"
        },
        {
            "id": 3,
            "movie_release_date": "Wed, 23 May 2012 00:00:00 GMT",
            "movie_title": "changed movie2"
        },
        {
            "id": 1,
            "movie_release_date": "Wed, 23 May 2012 00:00:00 GMT",
            "movie_title": "changed movie2"
        }
    ],
    "success": true
}
```

#### GET /movies/{id}
- General:
    - Returns a movie object

``` {
    "movie": {
        "id": 1,
        "movie_release_date": "Wed, 23 May 2012 00:00:00 GMT",
        "movie_title": "changed movie2"
    },
    "success": true
}
```

#### DELETE /actor/{question_id}
- General:
    - Deletes the movie of the given ID if it exists. Returns success or failure
```
{
  "success": true
}
```

#### POST /movies
- General:
    - Creates a new movie using the submitted question, answer, category and difficulty. Returns the success value. 
```
{
  "success": true,
}
```

#### PUT /movies
- General:
    - Updates a new movie using the submitted question, answer, category and difficulty. Returns the success value. 
```
{
  "success": true,
}
```

## Testing
To run the tests, run
```
python test_flaskr.py
```