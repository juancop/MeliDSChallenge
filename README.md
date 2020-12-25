# Data Science Challenge

El presente repositorio contiene un Reto Técnico de Data Science para Mercado Libre. A continuación se describe la organización del repositorio. Uno de los aportes más importantes es la creación de una clase que permite extraer los productos del Marketplace de **cualquier** país en el que opera Mercado Libre.

## Estructura del Repositorio

En el nivel más alto se encuentra `Download_Data.ipynb`, un Notebook que ejecuta el código para la descarga de información de los productos de Colombia.

El módulo ``src`` es el principal elemento del respositorio, pues contiene todos los códigos necesarios para la descarga de información. De esta forma, la descarga de información de cualquier país está completamente automatizada.

* `retrieve.py`: Contiene la clase que descarga automáticamente los productos del Marketplace para cualquier país deseado. 

* `token.py`: Genera automáticamente los Tokens de autenticación para superar los límites públicos del API. Utiliza el SDK MELI de Python.

La carpeta `notebooks` contiene los notebooks de análisis exploratorio y modelamiento. 

Finalmente, la carpeta `data` contiene los archivos descargados para Colombia, que son el insumo de la información de este reto.




## Toca poner información de las fuentes > Del país > Los artículos y las limitaciones en cuanto a requests
## También toca poner el tema de la organización y principales hallazgos.
