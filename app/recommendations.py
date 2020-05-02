import urllib.request
import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

url = 'https://raw.githubusercontent.com/codeheroku/Introduction-to-Machine-Learning/master/Building%20a%20Movie%20Recommendation%20Engine/movie_dataset.csv'
response = requests.get(url)
with urllib.request.urlopen(url) as testfile, open('dataset.csv', 'wb') as f:
    f.write(testfile.read().decode().encode("utf-8"))

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

movie_user_likes = "Iron Man"
movie_index = get_index_from_title(movie_user_likes)
similar_movies = list(enumerate(cosine_sim[movie_index])) #accessing the row corresponding to given movie to find all the similarity scores for that movie and then enumerating over it

sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

i=0
print("Top 5 similar movies to "+movie_user_likes+" are:\n")
for element in sorted_similar_movies:
    print(get_title_from_index(element[0]))
    i=i+1
    if i>4:
        break

