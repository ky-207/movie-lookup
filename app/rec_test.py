# TO BE DELETED!!

import os
import json

from dotenv import load_dotenv
import requests

import urllib.request
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

if __name__ == "__main__":

    #
    # INFO INPUTS
    #

    title = input("Please enter a movie or tv show title (i.e. 'Iron Man' or 'Game of Thrones'): ") # accept user input

    # how to replace whitespaces (source): https://stackoverflow.com/questions/1007481/how-do-i-replace-whitespaces-with-underscore-and-vice-versa
    title.replace(" ","+") # transforms the user input so that it is suitable for the request url later

    OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
    request_url = f"https://omdbapi.com/?s={title}&apikey={OMDB_API_KEY}"
    response = requests.get(request_url)

    # validating user's input
    if "\"Response\":\"False\"" in response.text:
        print("Oops, couldn't find that movie. Please try again.")
        exit()

    parsed_response = json.loads(response.text)

    sr = parsed_response["Search"] # search results


    # if there is more than one result, then the program will have the user choose the title they were looking for
    # from a list; otherwise, the program will go ahead and display the information of the one found result
    if int(parsed_response["totalResults"]) > 1:
        
        org_list = []

        for t in sr:
            org_list.append(t["Title"] + ", " + t["Year"])
            print(t["Title"] + " (" + t["Year"] +")") # prints a list of the search results' title and release year

        print("----------------------------------")
        correct_search = input("From the list above, what title were you looking for? Please write in the format of Title, Year (i.e. The Avengers, 1998): ")
        
        if (correct_search) in org_list:
            i = org_list.index(correct_search) # finds the index of the title the user is looking for in org_list so it can be matched with the one in the parsed_response
            id = sr[i]["imdbID"] 
        else:
            print("That's not an option from the list above. Please try again.")
    else:
        id = sr[0]["imdbID"]


    # make another request to match ids
    request_url = f"https://omdbapi.com/?i={id}&apikey={OMDB_API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    title_name = parsed_response["Title"]
    release_year = parsed_response["Year"]
    genre = parsed_response["Genre"]
    director = parsed_response["Director"]
    cast = parsed_response["Actors"]
    summary = parsed_response["Plot"]

    # rating preference on Rotten Tomatoes, but will resort to IMDb's rating if non-existent
    if "Rotten Tomatoes" in parsed_response["Ratings"][1]["Source"]:
        rating = "ROTTEN TOMATOES RATING: " + parsed_response["Ratings"][1]["Value"]
    else:
        rating = "IMDb RATING: " + parsed_response["Ratings"][0]["Value"]

    #
    # INFO OUTPUTS
    #

    print("----------------------------------")
    print(f"TITLE: {title_name} ({release_year})")
    print("----------------------------------")

    print(f"GENRE: {genre}")
    print(f"DIRECTOR: {director}")
    print(f"MAIN CAST: {cast}")
    print(f"SUMMARY: {summary}")
    print(rating)
    print("----------------------------------")


    #url = 'https://raw.githubusercontent.com/codeheroku/Introduction-to-Machine-Learning/master/Building%20a%20Movie%20Recommendation%20Engine/movie_dataset.csv'
    #response = requests.get(url)
    #with urllib.request.urlopen(url) as testfile, open('dataset.csv', 'wb') as f:
    #    f.write(testfile.read().decode().encode("utf-8"))

    correct_title = correct_search.split(", ")
    correct_name = correct_title[0]

    df = pd.read_csv("dataset.csv")
    features = ['keywords', 'cast', 'genres', 'director']

    def combine_features(row):
        return row['keywords']+" "+row['cast']+" "+row["genres"]+" "+row["director"]

    for feature in features:
        df[feature] = df[feature].fillna('')
    df["combined_features"] = df.apply(combine_features, axis=1)

    cv = CountVectorizer() #creating new CountVectorizer() object
    count_matrix = cv.fit_transform(df["combined_features"]) #feeding combined strings(movie contents) to CountVectorizer() object

    cosine_sim = cosine_similarity(count_matrix)

    def get_title_from_index(index):
        return df[df.index == index]["title"].values[0]
    def get_index_from_title(title):
        return df[df.title == title]["index"].values[0]

    #movie_user_likes = "Iron Man"
    while True:
        try:
            movie_index = get_index_from_title(correct_name)
            similar_movies = list(enumerate(cosine_sim[movie_index])) #accessing the row corresponding to given movie to find all the similarity scores for that movie and then enumerating over it

            sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

            i=0
            print("Top 5 similar movies to "+correct_name+" are:\n")
            for element in sorted_similar_movies:
                print(get_title_from_index(element[0]))
                i=i+1
                if i>4:
                    break
            break
        except IndexError:
            print("Sorry, we couldn't find any recommendations for that movie.")
            break


