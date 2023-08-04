#Se cargan las librerias necesarias para llevar a cabo la API y las funciones dentro de esta
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from fastapi import FastAPI, Form, Request
from enum import Enum
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


#DATA GENERAL DE LA API
app = FastAPI()
app.title = "Movies API - ML MoviesRecommenderSystem"
app.version = "1.0.0"

@app.on_event("startup")
async def startup_event():
    #Se cargan los nuevos dataset generados a partir del proceso de ETL 
    global df_movies
    global df_crew
    global movies_crew
    df_movies=pd.read_csv('data/new_movies.csv')
    df_crew=pd.read_csv('data/crew.csv')
    movies_crew=df_movies.merge(df_crew,how='inner',on='id')



@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo'''
    count=0
    for i in df_movies.name_lenguages:
        try:
            if type(eval(i))!=list:
                continue
            else:
                if idioma==eval(i)[0]:
                    count+=1
        except:
            continue
    return {'idioma':idioma, 'cantidad':count}
    
@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
    '''Ingresas la pelicula, retornando la duracion y el año'''
    lis=[]
    for i in df_movies.runtime[df_movies.title==pelicula]:
        lis.append(i)
    try:
        duracion=int(lis[0])
    except:
        duracion='No se encontro duración'
    try:
        anio=int(df_movies.release_year[df_movies.title==pelicula])
    except:
        anio=int(list(df_movies.release_year[df_movies.title==pelicula])[0])
        
    return {'pelicula':pelicula, 'duracion':duracion, 'anio':anio}



@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
    count=0
    lis_ganancia=[]
    for j,i in df_movies.name_collection.items():
        try:
            if franquicia==str(i):
                count+=1
                lis_ganancia.append(df_movies.iloc[1,6])                
            else:
                continue
        except:
            continue
    return {'franquicia':franquicia, 'cantidad':count, 'ganancia_total':sum(lis_ganancia), 'ganancia_promedio':np.mean(lis_ganancia)}

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''
    count=0
    for i in df_movies.name_countries:
        try:
            if type(eval(i))!=list:
                continue
            else:
                for h in eval(i):
                    if pais==str(h):
                        count+=1
                    else:
                        continue
        except:
            continue
    return {'pais':pais, 'cantidad':count}

@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''
    lis_revenue=[]
    count=0
    for j,i in df_movies.name_companies.items():
        try:
            if type(eval(i))!=list:
                continue
            else:
                for h in eval(i):
                    if productora==str(h):
                        lis_revenue.append(df_movies.revenue[j])
                        count+=1
                    else:
                        continue
        except:
            continue
    return {'productora':productora, 'revenue_total': sum(lis_revenue),'cantidad':count}


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    lis_return=[]
    titulos=[]
    año_estreno=[]
    presupuesto=[]
    ganancia=[]
    retorno=[]
    for j,i in movies_crew.name.items():
        if i==nombre_director:
            if movies_crew.job[j]=='Director':
                lis_return.append(movies_crew.iloc[j,26]) 
                titulos.append(movies_crew.title[j])
                retorno.append(round(movies_crew.iloc[j,26],5))
                año_estreno.append(int(movies_crew.release_year[j]))
                ganancia.append(round(movies_crew.revenue[j],5))
                presupuesto.append(round(movies_crew.budget[j],5))
    peliculas=[{'titulo': v1, 'año_lanzamiento': v2, 'presupuesto': v3, 'ganancia': v4, 'retorno':v5} for v1, v2, v3,v4,v5 in zip(titulos, año_estreno, presupuesto, ganancia, retorno)]
    if len(lis_return)==0:
        outcome= 'No se encontro director'
    else:
        outcome={'Director':nombre_director, 'retorno':round(sum(lis_return),5),'peliculas:':peliculas}
    return outcome

# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(title:str):
    new_datos=df_movies[0:5000]
    new_datos.reset_index
    for j,i in new_datos['name_genres'].items():
        new_datos['name_genres'][j]=i.replace(",", "").replace("[", "").replace("]", "").replace("'", "")
    new_datos['union_texto']=new_datos['name_genres'] + ' ' + new_datos['title']   + ' ' + new_datos['overview']
    for j,i in new_datos['union_texto'].items():
        if type(i) ==float:
            new_datos['union_texto'][j]='-'
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(new_datos['union_texto'])
    matrix_cosine=cosine_similarity(tfidf_matrix, tfidf_matrix)
    idx=new_datos.index[new_datos['title']==title][0]
    sim_scores = list(enumerate(matrix_cosine[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:10+1]]
    top_movies = new_datos['title'].iloc[top_indices].values
    return('El top 10 de peliculas recomendadas son las siguientes:',top_movies)

