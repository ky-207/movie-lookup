# app/seach_service.py

import os
import json

from dotenv import load_dotenv
import requests

load_dotenv()

#
# INFO INPUTS
#

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
request_url = f"https://omdbapi.com/?t=Iron+Man&apikey={OMDB_API_KEY}"
response = requests.get(request_url)
parsed_response = json.loads(response.text)

title = parsed_response["Title"]
release_year = parsed_response["Year"]
genre = parsed_response["Genre"]
director = parsed_response["Director"]
cast = parsed_response["Actors"]
summary = parsed_response["Plot"]
rating = parsed_response["Ratings"][1]["Value"]

print(f"TITLE: {title} ({release_year})")
print(f"GENRE: {genre}")
print(f"DIRECTOR: {director}")
print(f"MAIN CAST: {cast}")
print(f"SUMMARY: {summary}")
print(f"ROTTEN TOMATOES RATING: {rating}")