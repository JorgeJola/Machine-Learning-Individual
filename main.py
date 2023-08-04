#Se cargan las librerias necesarias para llevar a cabo la API y las funciones dentro de esta
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

#Se cargan los nuevos dataset generados a partir del proceso de ETL 
df_movies=pd.read_csv('data/new_movies.csv')
df_crew=pd.read_csv('data/crew.csv')
df_cast=pd.read_csv('data/cast.csv')
movies_cast=df_movies.merge(df_cast, how='inner',on='id')
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
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    lis_return=[]
    print(f'El/la director@ {nombre_director} dirijio peliculas como:')
    for j,i in movies_crew.name.items():
        if i==nombre_director:
            if movies_crew.job[j]=='Director':
                lis_return.append(movies_crew.iloc[j,26]) 
                print(f'{movies_crew.title[j]} con un retorno de {round(movies_crew.iloc[j,26],5)}, esta pelicula fue lanzada en el año {int(movies_crew.release_year[j])} teniendo un costo de {round(movies_crew.budget[j],5)} y una ganancia de {round(movies_crew.revenue[j],5)}')         
    if len(lis_return)==0:
        return(f'No se encontraron peliculas para este director')
    else:
        return(f'El actor consiguio un retorno total de {round(sum(lis_return),5)}')

# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(title:str):
    new_datos=df_movies[0:5000]
    new_datos.reset_index
    new_datos['union_texto']=new_datos['name_genres'] + ' ' + new_datos['title']   + ' ' + new_datos['overview']
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(new_datos['union_texto'])
    matrix_cosine=cosine_similarity(tfidf_matrix, tfidf_matrix)
    idx=new_datos.index[new_datos['title']==title][0]
    sim_scores = list(enumerate(matrix_cosine[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:10+1]]
    top_movies = new_datos['title'].iloc[top_indices].values
    return(top_movies)

