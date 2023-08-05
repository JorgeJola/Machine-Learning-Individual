import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.neighbors import NearestNeighbors

def matrix(df):
    for j,i in df['name_genres'].items():
        df['name_genres'][j]=i.replace(",", "").replace("[", "").replace("]", "").replace("'", "")
    df['union_texto']=df['name_genres'] + ' ' + df['title']   + ' ' + df['overview']
    for j,i in df['union_texto'].items():
        if type(i) ==float:
            df['union_texto'][j]='-'
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['union_texto'])
    matrix_cosine=cosine_similarity(tfidf_matrix, tfidf_matrix)
    return matrix_cosine