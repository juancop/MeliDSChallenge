# Data Science Challenge

El presente repositorio contiene un Reto Técnico de Data Science para Mercado Libre. A continuación se describe la organización del repositorio. Uno de los aportes más importantes es la creación de una clase que permite extraer los productos del Marketplace de **cualquier** país en el que opera Mercado Libre.

## Estructura del Repositorio

En el nivel más alto se encuentra `Download_Data.ipynb`, un Notebook que ejecuta el código para la descarga de información de los productos de Colombia.

El módulo ``src`` es el principal elemento del respositorio, pues contiene todos los códigos necesarios para la descarga de información. De esta forma, la descarga de información de cualquier país está completamente automatizada.

* `retrieve.py`: Contiene la clase que descarga automáticamente los productos del Marketplace para cualquier país deseado. 

* `token.py`: Genera automáticamente los Tokens de autenticación para superar los límites públicos del API. Utiliza el SDK MELI de Python.

La carpeta `notebooks` contiene los notebooks de análisis exploratorio y modelamiento. 

* `AnalisisExploratorio.ipynb`: Contiene la solución de la primera parte del Desafío (Análisis Exploratorio de Productos con Descuento)

* `EDA_SoldQuantity.ipynb`: Contiene el Análisis Exploratorio para la creación del modelo de predicción de Cantidad Vendida (*sold_quantity*).

* `MODEL_SoldQuantity.ipynb`: Es el Notebook que realiza la estimación de modelos y su evaluación. 

Finalmente, la carpeta `data` contiene los archivos descargados para Colombia, que son el insumo de la información de este reto, y la carpeta `imgs` guarda imágenes que son utilizadas dentro de los Notebooks de exploración.


