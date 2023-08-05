import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.neighbors import NearestNeighbors

def matrix(df):
    df['union_texto']=df['name_genres'] + ' ' + df['title']   + ' ' + df['overview']
    for j,i in df['union_texto'].items():
        if type(i) ==float:
            df['union_texto'][j]='-'
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['union_texto'])
    matrix_cosine=cosine_similarity(tfidf_matrix, tfidf_matrix)
    return matrix_cosine

def recomendacion(indice_pelicula, matriz_sim, df, top_n=5):
    #Dada la correspondencia de los indices del df con la matriz me quedo con los puntajes de similitud en torno a esa pelicula
    sim_scores = list(enumerate(matriz_sim[indice_pelicula]))
    #Ordeno de mayor a menor los scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #Selecciono lo más similares en funcion de top_n, evadiendo el primero que corresponde a la misma pelicula
    top_indices = [i[0] for i in sim_scores[1:top_n+1]]

    #Me quedo con los titulos y la similitud
    top_movies = df['title'].iloc[top_indices].values
    # scores = sim_scores[1:top_n+1]
    return top_movies