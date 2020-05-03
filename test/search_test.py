import pytest
import os

from app.search_service import get_response, youtube_search

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

def test_youtube_search():
    options = "Iron Man"

    assert youtube_search(options) == "https://www.youtube.com/watch?v=8ugaeA-nMTc"