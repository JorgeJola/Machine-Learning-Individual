#Se cargan las respectivas librerias a utilizar para el proceso de ETL (Extracción, transformación y carga)
import pandas as pd
import numpy as np
from datetime import datetime
import csv

#Se cargan ambos datasets con la información del proyecto y haciendo uso de PANDAS
movies=pd.read_csv('movies_dataset.csv')
credits=pd.read_csv('credits.csv')
##Se va a empezar por el proceso de limpieza del dataset movies por lo que se visualizan los datos y las variables

##Se visualizan features del dataset
print(movies.columns)
##Se hace una visualización general de las primeras filas del dataset
print(movies.head())

#Features que deben ser modificadas: belongs_to_collection, genres, production_companies, production_countries, spoken_lenguages

#Durante las siguientes modificaciones donde campos como belong_to_collection son campos anidados se hizo uso de la función eval()
#para manipular estos campos y con ayuda de la función for() se recorrieron todas las filas guardando cada uno de los fragmentos de 
#las partes anidadas en una variables creando nuevas feature o columnas dentro deldata-frame, se hizo uso tambien de condicionales
# los cuales permitian distinguir entre diferentes clases de datos y hacer una mejor manipulación de estos mismos.

#Modificación de belong_to_collection - En esta columna se encontraron valores extraños (sin sentido) que fueron eliminados agrupandolos
# en una lista como se puede ver a continuación en el primer condicional.
id_collection=[]
name_collection=[]
poster_path_collection=[]
backdrop_path_collection=[]

for j,i in movies.belongs_to_collection.iteritems():
    if type(i)==float or i in ['nan','0.065736','1.931659','2.185485']:
        id_collection.append(float('nan'))
        name_collection.append(float('nan'))
        poster_path_collection.append(float('nan'))
        backdrop_path_collection.append(float('nan'))
    else:
        id_collection.append(int(eval(movies.belongs_to_collection[j])['id']))
        name_collection.append(eval(movies.belongs_to_collection[j])['name'])
        poster_path_collection.append(eval(movies.belongs_to_collection[j])['poster_path'])
        backdrop_path_collection.append(eval(movies.belongs_to_collection[j])['backdrop_path'])

movies['id_collection']=id_collection
movies['name_collection']=name_collection
movies['poster_path_collection']=poster_path_collection
movies['backdrop_path_collection']=backdrop_path_collection

movies=movies.drop('belongs_to_collection', axis=1)

#Modificación de genres, esta modificación fue sencilla ya que no se encontraron valores extraños y crearon dos nuevos columnas generadas
# a partir de listas como lo son id_genres y name_genres
id_genres=[]
name_genres=[]
lis=[]
lis_n=[]
for i in movies.genres:
    for j in eval(i):
        lis.append(j['id'])
        lis_n.append(j['name'])
    id_genres.append(lis)
    name_genres.append(lis_n)
    lis=[]
    lis_n=[]
movies['id_genres']=id_genres
movies['name_genres']=name_genres

movies=movies.drop('genres', axis=1)

#Modificación production_companies, en esta columna se encontraron listas vacias que no las contaba diferctamente como valores nulos 
#por lo que con ayuda de un condicional se lograron separar y convertir en valores nulos
id_companies=[]
name_companies=[]
lis=[]
lis_n=[]
for i in movies.production_companies:
    if type(i)==str:
        if i =='[]':
            lis.append(float('nan'))
            lis_n.append(float('nan'))
        elif type(eval(i)) ==bool:
            lis.append(float('nan'))
            lis_n.append(float('nan'))
        else:
            for j in eval(i):
                lis.append(j['id'])
                lis_n.append(j['name'])
    else:
        lis.append(float('nan'))
        lis_n.append(float('nan'))
    id_companies.append(lis)
    name_companies.append(lis_n)
    lis=[]
    lis_n=[]
movies['id_companies']=id_companies
movies['name_companies']=name_companies

movies=movies.drop('production_companies', axis=1)

#Modificación production_countries, en esta columna hubo presencia de listas vacias no tomadas como valores nulos, tambien habian valores
#nulos tipo booleanos (bool) al ser convertidos por la funcion eval que con ayuda de condicionales se lograron filtrar todos estos valor y
#categorizar como nulos
iso_countries=[]
name_countries=[]
lis=[]
lis_n=[]
for i in movies.production_countries:
    if type(i)==str:
        if i =='[]':
            lis.append(float('nan'))
            lis_n.append(float('nan'))
        elif type(eval(i)) ==bool:
            lis.append(float('nan'))
            lis_n.append(float('nan'))
        elif type(eval(i)) ==float:
            lis.append(float('nan'))
            lis_n.append(float('nan'))
        else:
            for j in eval(i):
                lis.append(j['iso_3166_1'])
                lis_n.append(j['name'])
    else:
        lis.append(float('nan'))
        lis_n.append(float('nan'))
    iso_countries.append(lis)
    name_countries.append(lis_n)
    lis=[]
    lis_n=[]

movies['iso_countries']=iso_countries
movies['name_countries']=name_countries

movies=movies.drop('production_countries', axis=1)

#Modificación spoken_lenguages, en esta columna tambien se encontraron valores nulos de distinto tipo que fueron filtrados y categorizados
#con condicionales
iso_lenguages=[]
name_lenguages=[]
lis=[]
lis_n=[]
for i in movies.spoken_languages:
    if type(i)==str:
        if i =='[]':
            lis.append(float('nan'))
            lis_n.append(float('nan'))
        elif type(eval(i)) ==bool:
            lis.append(float('nan'))
            lis_n.append(float('nan'))
        elif type(eval(i)) ==float:
            lis.append(float('nan'))
            lis_n.append(float('nan'))
        else:
            for j in eval(i):
                lis.append(j['iso_639_1'])
                lis_n.append(j['name'])
    else:
        lis.append(float('nan'))
        lis_n.append(float('nan'))
    iso_lenguages.append(lis)
    name_lenguages.append(lis_n)
    lis=[]
    lis_n=[]

movies['iso_lenguages']=iso_lenguages
movies['name_lenguages']=name_lenguages

movies=movies.drop('spoken_languages', axis=1)

#En las anteriores modificaciones se eliminaron las columnas originales que fueron reemplazadas por nuevas columnas donde los datos
#se encuentran desanidados, algunos campos donde peliculas tienen mas de un datos se dejaron como listas ya que se considera que esto
#facilitara su posterior manejo

#Los valores nulos de los campos revenue, budget se rellenaron por el número 0 con ayuda de la función fillna.
movies.revenue.fillna(0, inplace=True)
movies.budget.fillna(0, inplace=True)

#Con ayuda de la funcion striptime de la libreria datetime cargada al inicio del script la columna release_date paso a tener 
#un formato AAAA-mm-dd, habia presencia de valores sin sentido que fueron filtrados por una lista en el primer condicional.
release_date=[]
for i in movies.release_date:
    if type(i)!=str or i in ['1','12','22']:
        release_date.append(float('nan'))
    else:
        release_date.append(datetime.strptime(i, "%Y-%m-%d"))

movies['release_date']=release_date

#Se creo la columna release_year donde se extrajo el año (.year) de la fecha de estreno de las peliculas de la columna release_date 
release_year=[]
for i in movies.release_date:
    release_year.append(i.year)
movies['release_year']=release_year

#Se creo la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas 
# revenue / budget, al no haber datos disponibles en algunos campos estos fueron reemplazados por 0. Aveces se podian presentar
#errores debido a algunos datos por lo que se utilizo try/except para que el for pudiera recorrer y anexar a la nueva columna return
#la totalidad de las filas.
return_=[]
for i in range(0,len(movies)+1):
        try:
            if float(movies.budget[i])==0:
                x=0
            else:
                x=float(movies.revenue[i])/float(movies.budget[i])
            return_.append(x)
        except:
            try:
                if type(movies.budget[i])==str:
                    return_.append(0)  
            except:
                 continue

movies['return']=return_

#Los valores nulos del campo release_date fueron eliminados con ayuda de la función drop.na()
movies.dropna(subset=['release_date'],inplace=True)

#Finalmente para este dataset movies se eliminaron columnas innecesarias con ayuda de la función .drop
#Las columnas eliminadas fueron: video, imdb_id, adult, original_title, poster_path y homepage.
columnas_a_eliminar = ['video','imdb_id','adult','original_title','poster_path', 'homepage','poster_path_collection','backdrop_path_collection']
movies = movies.drop(columnas_a_eliminar, axis=1)

#Asi quedaria el dataset final de movies
print(movies.columns)

#Para los siguientes procesos se guardo el nuevo dataset de movies como new_movies ya con todas las correciones pertinentes 
#realizadas anteriormente
#movies.to_csv('new_movies.csv', index=False)





##Continuamos con el proceso de limpieza del dataset credits por lo que se visualizan los datos y las variables

##Se visualizan features del dataset
print(credits.columns)
##Se hace una visualización general de las primeras filas del dataset
print(credits.head())

#Nos damos cuenta de que el dataframe credits posee dos columnas correspondientes a crew y cast por lo que a continuación se decide
#desanidar estos campos y generar 2 dataset (crew y cast)

#Se decide empezar con la formación del dataset cast, para esto nos damos cuenta de que los diccionarios que contienen los datos de
# este dataset tienen como keys: id, cast_id, character, credit_id, gender, id_actor, name, order, profile_path, id, cast_id.
# Por lo que se crean listas para guardar estas variables. Se cambio el nombre de la variable id a id_actor para evitar confusiones.
id=[]
cast_id=[]
character=[]
credit_id=[]
gender=[]
id_actor=[]
name=[]
order=[]
profile_path=[]

#Posteriormente para desanidar los diccionarios se utiliza un for que recorre toda la columna
for x,i in credits.cast.iteritems():
    for j in eval(i):
        id.append(credits.id[x])
        cast_id.append(j['cast_id'])
        character.append(j['character'])
        credit_id.append(j['credit_id'])
        gender.append(j['gender'])
        id_actor.append(j['id'])
        name.append(j['name'])
        order.append(j['order'])
        profile_path.append(j['profile_path']) 

#Se crea el dataframe cast y se le asignan las variables creadas anteriormente como listas
cast=pd.DataFrame()
cast['id']=id
cast['cast_id']=cast_id
cast['character']=character
cast['gender']=gender
cast['id_actor']=id_actor
cast['name']=name
cast['order']=order
cast['profile_path']=profile_path

#Se elimina columnas que se consideran innecesarias ya que no se van a tener en cuenta en los siguientes procesos
columnas_a_eliminar = ['profile_path','order']
cast = cast.drop(columnas_a_eliminar, axis=1)
#Se exportan los datos a csv
#cast.to_csv('cast.csv', index=False)  

#Se sigue con la formación del dataset crew, para esto nos damos cuenta de que los diccionarios que contienen los datos de
# este dataset tienen como keys: id, department, job, credit_id, gender, id_crew, name, order, profile_path.
# Por lo que se crean listas para guardar estas variables. Se cambio el nombre de la variable id a id_crew para evitar confusiones.
id=[]
department=[]
job=[]
credit_id=[]
gender=[]
id_crew=[]
name=[]
profile_path=[]

for x,i in credits.crew.iteritems():
    for j in eval(i):
        id.append(credits.id[x])
        credit_id.append(j['credit_id'])
        department.append(j['department'])
        gender.append(j['gender'])
        id_crew.append(j['id'])
        job.append(j['job'])
        name.append(j['name'])
        profile_path.append(j['profile_path'])

crew=pd.DataFrame()
crew['id']=id
crew['credit_id']=credit_id
crew['department']=department
crew['gender']=gender
crew['id_crew']=id_crew
crew['job']=job
crew['name']=name
crew['profile_path']=profile_path

#Se elimina columnas que se consideran innecesarias ya que no se van a tener en cuenta en los siguientes procesos
columnas_a_eliminar = ['profile_path','credit_id']
crew = crew.drop(columnas_a_eliminar, axis=1)
#Se exportan los datos a csv
#crew.to_csv('crew.csv', index=False)