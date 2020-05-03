# test/search_test.py

from app.search_service import youtube_search

def test_youtube_search():
    options = "Iron Man"

    assert youtube_search(options) == "https://www.youtube.com/watch?v=8ugaeA-nMTc"