import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.neighbors import NearestNeighbors

def matrix(df):
    #Se genera la columa con el texto de entrada
    df['texto_combinado'] = df['name_genres'].apply(lambda x: ' '.join(x)) + ' ' + df['title']   + ' ' + df['overview']
    #Elimino los signos de puntuacion
    df['texto_combinado'] = df['texto_combinado'].apply( lambda x: re.sub(r'[^\w\s]', '', x) if pd.notnull(x) else '' )

    # Crear una matriz TF-IDF a partir de los datos empleando las stop words en idioma ingles
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['texto_combinado'])

    #Se genera la matriz de similitud del coseno a partir de la matriz anterior
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    return cosine_sim

def recomendacion(indice_pelicula, matriz_sim, df):
    #Dada la correspondencia de los indices del df con la matriz me quedo con los puntajes de similitud en torno a esa pelicula
    sim_scores = list(enumerate(matriz_sim[indice_pelicula]))
    #Ordeno de mayor a menor los scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #Selecciono lo más similares en funcion de top_n, evadiendo el primero que corresponde a la misma pelicula
    top_indices = [i[0] for i in sim_scores[1:5+1]]

    #Me quedo con los titulos y la similitud
    top_movies = df['title'].iloc[top_indices].values
    # scores = sim_scores[1:top_n+1]
    return top_movies #, top_indices, scores