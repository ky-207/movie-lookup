# test/search_test.py

import pytest
import os

from app.search_service import get_response, get_response_2, print_sr, title_except, youtube_search

CI_ENV = os.environ.get("CI") == "true" # expect default environment variable setting of "CI=true" on Travis CI, see: https://docs.travis-ci.com/user/environment-variables/#default-environment-variables

@pytest.mark.skipif(CI_ENV==True, reason="to avoid configuring credentials on, and issuing requests from, the CI server")
def test_get_response():
    title = "Iron Man"

    parsed_response = get_response(title)

    assert isinstance(parsed_response, dict)
    assert "Search" in parsed_response.keys()
    assert "totalResults" in parsed_response.keys()
    assert "Response" in parsed_response.keys()
    assert parsed_response["Response"] == "True"

def test_get_response_2():
    id = "tt0371746"

    parsed_response = get_response_2(id)

    assert isinstance(parsed_response, dict)
    assert "Title" in parsed_response.keys()
    assert "Year" in parsed_response.keys()
    assert "Genre" in parsed_response.keys()
    assert "Director" in parsed_response.keys()
    assert "Actors" in parsed_response.keys()
    assert "Plot" in parsed_response.keys()
    assert "Ratings" in parsed_response.keys()
    assert parsed_response["Response"] == "True"

def test_print_sr():
    search_results = [
        {"Title":"Iron Man","Year":"2008","imdbID":"tt0371746","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BMTczNTI2ODUwOF5BMl5BanBnXkFtZTcwMTU0NTIzMw@@._V1_SX300.jpg"},
        {"Title":"Iron Man 3","Year":"2013","imdbID":"tt1300854","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BMjE5MzcyNjk1M15BMl5BanBnXkFtZTcwMjQ4MjcxOQ@@._V1_SX300.jpg"},
        {"Title":"Iron Man 2","Year":"2010","imdbID":"tt1228705","Type":"movie","Poster":"https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_SX300.jpg"}
    ]

    readable_list = []

    print_sr(search_results, readable_list)

    assert readable_list == [
        "Iron Man, 2008",
        "Iron Man 3, 2013",
        "Iron Man 2, 2010"
    ]

def test_title_except():
    s = "Hi, my name is John Smith"
    exceptions = ["a", "an", "is"]

    assert title_except(s, exceptions) == "Hi, My Name is John Smith"

def test_youtube_search():
    options = "Iron Man"

    assert youtube_search(options) == "https://www.youtube.com/watch?v=8ugaeA-nMTc"