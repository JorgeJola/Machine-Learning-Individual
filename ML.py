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

def recomendacion(title:str,new_datos,my_matrix):
    idx=new_datos.index[new_datos['title']==title][0]
    sim_scores = list(enumerate(my_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:10+1]]
    top_movies = new_datos['title'].iloc[top_indices].values
    return('El top 10 de peliculas recomendadas son las siguientes:',top_movies)