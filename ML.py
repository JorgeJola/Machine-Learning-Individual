import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.neighbors import NearestNeighbors

def matrix(df):
    #Se genera la columna de texto compuestas por variables con palabras clave
    df['texto_combinado'] = df['name_genres'] + ' ' + df['title']   + ' ' + df['overview']
    #Se eliminan signos de puntuación y signos no relevantes para el analisis
    df['texto_combinado'] = df['texto_combinado'].apply( lambda x: re.sub(r'[^\w\s]', '', x) if pd.notnull(x) else '' )

    # Se crea una matriz TF-IDF haciendo uso de los datos y utilizando stop words en ingles
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['texto_combinado'])

    #Una vez creada la matriz anterior se pasa como argumento en la funcion cosine_similarity para crear la matriz de similitus del coseno
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    return cosine_sim

def recomendacion(indice_pelicula, matriz_sim, df):
    #Ya teniendo la coincidencia entre los indices del dataframe con la matriz se enumeran y se guardan los puntajes 
    sim_scores = list(enumerate(matriz_sim[indice_pelicula]))
    #Una ves enumerados se ordenan de mayor a menor los puntajes
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #Se seleccionan los 5 primeros a excepción del 1 que hace referencia a la misma pelicula
    top_indices = [i[0] for i in sim_scores[1:5+1]]

    #Tomo los titulos de los 5 primeros puntajes
    top_movies = df['title'].iloc[top_indices].values
    return top_movies 