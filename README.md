![HenryLogo](https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png)

# **Machine Learning Operations (MLOps)**

¡Saludos! Soy Jorge Andrés Jola Hernández, y te presento una guía detallada de mi primer proyecto individual llevado a cabo en Henry. A lo largo de esta guía, te conduciré a través de cada paso que tomé en el proyecto, desde la depuración de los datos hasta la creación de una API completamente funcional con un modelo recomendador de películas.

Durante este proceso, abordé una serie de fases cruciales para lograr implementar con éxito el despliegue en la API y obtener un Producto Mínimo Viable (MVP). El punto de partida de este proceso fue la ejecución de una tarea de Extracción, Transformación y Carga (ETL).

# **ETL (Extract, Transform and Load)**
En esta etapa inicial, se comenzó con los conjuntos de datos en su estado original, los cuales contenían información tanto sobre películas (movies_dataset.csv) como sobre equipos de filmación (credits.csv). A través de una serie de transformaciones exhaustivas en estos conjuntos de datos, se logró llegar a un conjunto depurado y refinado que facilitó la creación tanto de funciones de consulta como del sistema de recomendación incorporados en la API.
Los datasets completo los puedes encontrar aqui https://drive.google.com/drive/folders/1t0eoBDPgGpy1O8OphfIK9IyIuOhhXUzK?usp=drive_link
## **Limpieza y tranformaciones del dataset movies.csv**

Dentro del conjunto de datos de movies.csv, se identificaron columnas con información detallada anidada que estaba vinculada a elementos específicos, como colecciones, géneros de películas, compañías de producción y lenguajes de las películas. Estos datos anidados necesitaban ser desglosados y distribuidos en columnas individuales para permitir un acceso más sencillo durante las etapas subsiguientes del proceso.

En estas columnas anidadas también se encontraron valores inconsistentes o sin sentido, que posiblemente resultaron de errores de entrada. Durante el proceso de limpieza, estos valores fueron tratados como nulos y corregidos en consecuencia. Además, en el caso de variables numéricas como el presupuesto `budget` y los ingresos `revenue`, los valores faltantes se sustituyeron por ceros.

Se introdujeron nuevas columnas derivadas de las existentes, como es el caso de las variables `release_year` y `return`. Finalmente, se depuraron las filas en las que la variable 'release_date' carecía de información, y se eliminaron aquellas columnas que no aportarían mucho valor en las etapas posteriores del proceso. Este último paso tenía como objetivo reducir el tamaño de los nuevos conjuntos de datos, lo cual resultaba beneficioso para trabajar en un entorno con limitaciones de recursos. El dataset final obtenido fue el siguiente: [new_movies.csv](https://github.com/JorgeJola/PI_ML_OPS-JorgeJola/blob/main/data/new_movies.csv)
## **Limpieza y tranformaciones del dataset credits.csv**
Dentro de este conjunto de datos, se identificaron dos columnas que almacenaban información distinta. La primera columna contenía datos relacionados con el elenco de la película, incluyendo información sobre los actores involucrados. En contraste, la segunda columna contenía detalles sobre el equipo de producción, que abarcaba a los directores y otros miembros del equipo de filmación.

Para abordar esta estructura, se llevó a cabo un proceso de desanidamiento, mediante el cual la información de ambas columnas fue separada y organizada en dos conjuntos de datos diferentes. Sin embargo, para las etapas subsiguientes del proceso, se optó por utilizar únicamente uno de estos conjuntos de datos (crew.csv). Esta ultimo dataset fue filtrado obteniendo un dataset que contenia unicamente informacion de los directores [df_directores.csv](https://github.com/JorgeJola/PI_ML_OPS-JorgeJola/blob/main/data/df_directores.csv).

Vea proceso de ETL completo en: [ETL.py](https://github.com/JorgeJola/PI_ML_OPS-JorgeJola/blob/main/ETL.py)

## **EDA (Análisis Descriptivo)**
Se realizó un análisis descriptivo exhaustivo de los datos, lo que nos proporcionó una comprensión más profunda de nuestra información y su alcance. Durante este proceso, se llevaron a cabo visualizaciones para identificar patrones, distribuciones y posibles correlaciones en los datos. El Análisis Exploratorio de Datos se centró en las variables que se utilizarían más adelante en las funciones, brindando una visión clave sobre elementos como `names_genre`, `overview` y `title` de las películas, que posteriormente se utilizarían para desarrollar el modelo de recomendación.

Dentro del EDA, se presentan diversos tipos de gráficos, incluyendo gráficos de barras, gráficos de correlación, gráficos de dispersión y gráficos de series temporales. Estas visualizaciones permitieron realizar un análisis descriptivo en profundidad del conjunto de datos a nuestra disposición.

Vea proceso de ETL completo en: [EDA.ipynb](https://github.com/JorgeJola/PI_ML_OPS-JorgeJola/blob/main/EDA.ipynb)

## **Desarrollo de funciones de consulta**
A continuación, se han realizado seis funciones de consulta que permiten a cualquier usuario realizar búsquedas generando una entrada en cada una de estas funciones creadas. Aunque el código no ha sido comentado en el archivo [main.py](https://github.com/JorgeJola/PI_ML_OPS-JorgeJola/blob/main/main.py), se brindará una descripción superficial del funcionamiento de cada una de estas funciones. Las funciones realizadas son las siguientes:

`peliculas_idioma(idioma)`: En esta función, proporcionas el nombre del idioma exactamente como se escribe en dicho idioma (por ejemplo: English). La función devolverá la cantidad de películas producidas en ese idioma específico. La implementación de la función utiliza un bucle 'for' que recorre las listas de idiomas, identificando el primer idioma que corresponde al idioma en el que se filmó la película. Cada vez que se encuentra una coincidencia con el idioma, la variable contador (llamada 'count') va acumulando el número de películas realizadas en ese idioma.


`peliculas_duracion(pelicula)`: Dentro de esta función, introduces el nombre de la película (por ejemplo: Shrek) y obtendrás como resultado la duración de la película junto con el año en que fue estrenada. Para llevar a cabo su implementación, en primer lugar se identifican las columnas que contienen este titulo y se extraen tanto el año de estreno como la duración de variables preexistentes, tales como `release_year` y `runtime`.


`franquicia(franquicia)` :Dentro de esta función, introduces el nombre de la franquicia, es decir, el nombre de la colección (por ejemplo: Toy Story Collection), y obtendrás como resultado el número de películas que contiene, además de la ganancia total y promedio generada por dicha franquicia. Para llevar a cabo su implementación, se siguió un procedimiento similar al de la función anterior. En primer lugar, se identifican las filas que corresponden a la franquicia utilizando la variable `name_collection`, y la cantidad de películas se determina mediante la longitud de esta variable que contiene exclusivamente las filas relacionadas con la franquicia de entrada. Luego, se calcula la ganancia total empleando la función 'sum()', y para la ganancia promedio por película, se hace uso de la biblioteca numpy y su función 'np.mean()'.


`peliculas_pais(pais)`:


