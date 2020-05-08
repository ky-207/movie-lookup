# app/movie_lookup.py

import os
import json
import re
import webbrowser
import requests
import pandas as pd

from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.search_service import get_response, get_response_2, print_sr, title_except, youtube_search
from app.recommendations import combine_features, get_title_from_index, get_index_from_title, movie_recommendations
from app.to_watch_service import SpreadsheetService, user_options

load_dotenv()

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

if __name__ == "__main__":

    # search service
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

    parsed_response = get_response_2(id)

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

    # YouTube search
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

    # recommendations service
    while True:
        recs = input("Would you like to be recommended similar titles, if there are any? [Y/N] ")

        if recs.lower() == "y":
            df = pd.read_csv("dataset.csv")
            features = ['keywords', 'cast', 'genres', 'director']
            for feature in features:
                df[feature] = df[feature].fillna('')
            df["combined_features"] = df.apply(combine_features, axis=1)
            while True:
                try:
                    movie_recommendations(df, correct_name)
                    break
                except IndexError:
                    print("Sorry, we couldn't find any recommendations for that title.")
                    print("----------------------------------")
                    break
            break
        elif recs.lower() == "n":
            print("Okay, you opted not to get recommendations.")
            print("----------------------------------")
            break
        else: 
            print("Sorry, that was not a valid choice, please try again and enter 'Y' or 'N'.")

    # to watch service
    while True:
        watch = input(f"Would you like to add {title_name} to your To-Watch List? [Y/N] ")
        
        if watch.lower() == "y":
            ss = SpreadsheetService()
            sheet, movies = ss.get_movies()
            print("----------------------------------")
            print(f"LISTING TITLES FROM THE '{sheet.title}' SHEET")
            for movie in movies:
                print(" + " + str(movie["ID"]) + ": " + movie["Title"])
            movie_attributes = parsed_response
            response = ss.create_movie(movie_attributes)
            print("----------------------------------")
            print("CREATING A TITLE...")
            print("ADDED NEW TITLE: " + movie_attributes["Title"])
            print("----------------------------------")
            print(f"... UPDATED RANGE {response['updatedRange']} ({response['updatedCells']} CELLS)")
            while True:
                print("----------------------------------")
                sheet, movies = ss.get_movies()
                option = input("Would you like to: 1. Get a title; 2. Delete a title; 3. Clear list; 4. Exit? Please enter 1, 2, 3, or 4: ")
                user_options(option, ss)
        elif watch.lower() == "n":
            print(f"Okay, you opted not to add {title_name} to your To-Watch List.")
            print("----------------------------------")
            break
        else:
            print("Sorry, that was not a valid choice, please try again and enter 'Y' or 'N'.")