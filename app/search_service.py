# app/seach_service.py

import os
import json

from dotenv import load_dotenv
import requests

load_dotenv()

#
# INFO INPUTS
#

movie = input("Please enter a movie title (i.e. Iron Man): ") # accept user input

# how to replace whitespaces (source): https://stackoverflow.com/questions/1007481/how-do-i-replace-whitespaces-with-underscore-and-vice-versa
movie.replace(" ","+") # transforms the user input so that it is suitable for the request url later

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
request_url = f"https://omdbapi.com/?t={movie}&apikey={OMDB_API_KEY}"
response = requests.get(request_url)

if "\"Response\":\"False\"" in response.text:
    print("Oops, couldn't find that movie. Please try again.")
    exit()
parsed_response = json.loads(response.text)

title = parsed_response["Title"]
release_year = parsed_response["Year"]
genre = parsed_response["Genre"]
director = parsed_response["Director"]
cast = parsed_response["Actors"]
summary = parsed_response["Plot"]

if "Rotten Tomatoes" in parsed_response["Ratings"]:
    rating = parsed_response["Ratings"][1]["Value"]
else:
    rating = parsed_response["Ratings"][0]["Value"]

#
# INFO OUTPUTS
#

print(f"TITLE: {title} ({release_year})")
print(f"GENRE: {genre}")
print(f"DIRECTOR: {director}")
print(f"MAIN CAST: {cast}")
print(f"SUMMARY: {summary}")

if "Rotten Tomatoes" in parsed_response["Ratings"]:
    print(f"ROTTEN TOMATOES RATING: {rating}")
else:
    print(f"IMDb RATING: {rating}")
