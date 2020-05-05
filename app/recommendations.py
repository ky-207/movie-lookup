# app/recommendations.py
# Adapted from code sourced here: https://medium.com/code-heroku/building-a-movie-recommendation-engine-in-python-using-scikit-learn-c7489d7cb145

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def combine_features(row):
    """
    Combines the values in the columns into a single string.
    Example: df.apply(combine_features, axis=1)
    Returns: the combined string of each row in the dataset stored in the a new specified column
    """
    return row['keywords']+" "+row['cast']+" "+row["genres"]+" "+row["director"]
    
def get_title_from_index(df, index):
    """
    Returns the matching title of a movie from its index.
    Param: df (pandas function that reads a csv into a dataframe) like pd.read_csv("dataset.csv") and index (int) like element[0]
    Example: get_title_from_index(element[0])
    Returns: the title of the movie
    """
    return df[df.index == index]["title"].values[0]

def get_index_from_title(df, title):
    """
    Returns the matching index of a movie from its title.
    Param: df (pandas function that reads a csv into a dataframe) like pd.read_csv("dataset.csv") and title (str) like correct_name
    Example: get_index_from_title(correct_name)
    Returns: the index of the movie the user is searching for in the dataset
    """
    return df[df.title == title]["index"].values[0]

def movie_recommendations(df, title):
    """
    Returns the five movies that are similar to the movie the user has selected.
    Param: df (pandas function that reads a csv into a dataframe) like pd.read_csv("dataset.csv") and title (str) like correct_name
    Example: movie_recommendations(correct_name)
    Returns: five recommended movies
    """
    movie_index = get_index_from_title(df, title)
    similar_movies = list(enumerate(cosine_sim[movie_index])) #accessing the row corresponding to given movie to find all the similarity scores for that movie and then enumerating over it
    sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
    i=0
    print("Top 5 similar movies to "+title+" are:")
    for element in sorted_similar_movies:
        print(" + " + get_title_from_index(df, element[0]))
        i=i+1
        if i>4:
            print("----------------------------------")
            break

if __name__ == "__main__":

    # reads the dataset.csv into a dataframe
    df = pd.read_csv("dataset.csv")

    # fills all NaN files with blank string in the dataframe to clean and preprocess the data
    features = ['keywords', 'cast', 'genres', 'director']
    for feature in features:
        df[feature] = df[feature].fillna('')
    df["combined_features"] = df.apply(combine_features, axis=1) #applying combine_features() method over each rows of dataframe and storing the combined string in “combined_features” column
    
    cv = CountVectorizer() # creating new CountVectorizer() object
    count_matrix = cv.fit_transform(df["combined_features"]) # feeding combined strings(movie contents) to CountVectorizer() object
    cosine_sim = cosine_similarity(count_matrix)

    # attempts to find 5 movies similar to the movie the user has selected
    while True:
        try:
            movie_recommendations(df, correct_name)
            break
        except IndexError:
            print("Sorry, we couldn't find any recommendations for that movie.")
            print("----------------------------------")
            break
