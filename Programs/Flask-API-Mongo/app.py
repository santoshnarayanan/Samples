from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Movie

app = Flask(__name__)

movies = [
    {
        "name": "The Shawshank Redemption",
        "casts": ["Tim Robbins", "morgan Freeman", "Bob Gunton", "William Saadler"],
        "genres": ["Drama"]
    },

    {
        "name": "The GodFather",
        "casts": ["Marlon Brando", "Al Pacino", "James Caan", "Diane Keaton"],
        "genres": ["Drama"]
    }
]

app.config['MONGOD_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag'
}

initialize_db(app)


@app.route('/movies')
def hello():
    return jsonify(movies)


@app.route('/movies')
def get_movies():
    movies = Movie.objects().to_json()
    return Response(movies, mimetype="application/json", status=200)


@app.route('/movies', methods=['POST'])
def add_movie():
    movie = request.get_json();
    movies.append(movie)
    return {'id': len(movies)}, 200


@app.route('/movies/<int:index>',methods=['PUT'])
def update_movie(index):
    movie = request.get_json()
    movies[index]=movie
    return jsonify(movies[index]), 200


@app.route('/movies/<int:index>',methods=['DELETE'])
def delete_movie(index):
    movies.pop(index)
    return 'None',200

app.run()