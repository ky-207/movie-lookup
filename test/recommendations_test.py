# test/recommendations_test.py

import pytest
import os
import pandas as pd

from app.recommendations import combine_features, get_title_from_index, get_index_from_title, movie_recommendations

df = pd.read_csv("dataset.csv")

def test_combine_features():
    features = ['keywords', 'cast', 'genres', 'director']
    for feature in features:
        df[feature] = df[feature].fillna('')

    df["combined_features"] = df.apply(combine_features, axis=1)

    assert df["combined_features"][0] == "culture clash future space war space colony society Sam Worthington Zoe Saldana Sigourney Weaver Stephen Lang Michelle Rodriguez Action Adventure Fantasy Science Fiction James Cameron"

def test_get_title_from_index():
    index = 0
    title = get_title_from_index(df, index)
    assert title == "Avatar"

def test_get_index_from_title():
    title = "Avatar"
    index = get_index_from_title(df, title)
    assert index == 0

#def test_movie_recommendations():