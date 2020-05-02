import urllib.request
import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#url = 'https://raw.githubusercontent.com/codeheroku/Introduction-to-Machine-Learning/master/Building%20a%20Movie%20Recommendation%20Engine/movie_dataset.csv'
#response = requests.get(url)
#with urllib.request.urlopen(url) as testfile, open('dataset.csv', 'wb') as f:
#    f.write(testfile.read().decode().encode("utf-8"))

filename = 'movie_dataset.csv'
df = pd.read_csv(filename)

