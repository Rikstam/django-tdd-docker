import json
import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    response = client.post(
        "/api/movies/",
        {
            "title": "Kummeli Stories",
            "genre": "comedy",
            "year": "1993",
        },
        content_type="application/json"
    )
    assert response.status_code == 201
    assert response.data["title"] == "Kummeli Stories"

    movie = Movie.objects.get(title__exact="Kummeli Stories")
    assert movie.title == "Kummeli Stories"


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    response = client.post(
        "/api/movies/",
        {},
        content_type="application/json"
    )
    assert response.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
        },
        content_type="application/json"
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    response = client.get(f"/api/movies/{movie.id}/")
    assert response.status_code == 200
    assert response.data["title"] == "The Big Lebowski"


@pytest.mark.django_db
def test_get_single_movie_incorrect_id(client):
    response = client.get(f"/api/movies/123/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="The Big Lebowski",
                          genre="comedy", year="1998")
    movie_two = add_movie("No Country for Old Men", "thriller", "2007")
    resp = client.get(f"/api/movies/")
    assert resp.status_code == 200
    assert resp.data[0]["title"] == movie_one.title
    assert resp.data[1]["title"] == movie_two.title
