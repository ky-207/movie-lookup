# app/movie_lookup.py

import os
from dotenv import load_dotenv

from app import APP_ENV
from app.search_service import get_response, print_sr, title_except, youtube_search
#from app.recommendations import combine_features, get_title_from_index, get_index_from_title, movie_recommendations
#from app.to_watch_service import SpreadsheetService, user_options

load_dotenv()

if __name__ == "__main__":

    title = input("Please enter a movie or tv show title (i.e. 'Iron Man' or 'Game of Thrones'): ")
    parsed_response = get_response(title)
    sr = parsed_response["Search"]

    if int(parsed_response["totalResults"]) > 1:
        org_list = []
        print_sr(sr, org_list)
        print("----------------------------------")
        while True:
            correct_search = input("From the list above, what title were you looking for? Please write in the format of Title, Year (i.e. The Avengers, 1998): ")
            articles = ['a', 'an', 'of', 'the', 'is', 'with', 'in']
            correct_search = title_except(correct_search, articles)
            correct_title = correct_search.split(", ")
            correct_name = correct_title[0]
            if (correct_search) in org_list:
                i = org_list.index(correct_search) 
                id = sr[i]["imdbID"] 
                break
            else:
                print("Sorry, there was no match to the list above. Please try again and make sure you're writing in the correct format.")
    else:
        id = sr[0]["imdbID"]
        correct_name = title
        correct_search = title

    request_url = f"https://omdbapi.com/?i={id}&apikey={OMDB_API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    title_name = parsed_response["Title"]
    release_year = parsed_response["Year"]
    genre = parsed_response["Genre"]
    director = parsed_response["Director"]
    cast = parsed_response["Actors"]
    summary = parsed_response["Plot"]
    rating = parsed_response["Ratings"][0]["Value"]

    print("----------------------------------")
    print(f"TITLE: {title_name} ({release_year})")
    print("----------------------------------")
    print(f"GENRE: {genre}")
    print(f"DIRECTOR: {director}")
    print(f"MAIN CAST: {cast}")
    print(f"SUMMARY: {summary}")
    print(f"IMDb RATING: {rating}")
    print("----------------------------------")

    while True:
        youtube = input(f"Would you like to see a trailer for {title_name}? [Y/N] ")
        if youtube.lower() == "y":
            print("Okay, pulling up trailer now...")
            url = youtube_search(correct_search)
            webbrowser.open(url)
            break
        elif youtube.lower() == "n":
            print("Okay, you opted not to watch the trailer.")
            print("----------------------------------")
            break
        else:
            print("Sorry, that was not a valid choice, please try again and enter 'Y' or 'N'.")