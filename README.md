# Science_News_Scrapy

## Descripción
------------
Scrapper realizado como conjunto de trabajo para el proyecto 3 de Platzi Master Cohort 7, en el que se realiza extracción de información de la web, de varias paginas de noticias. El scrapper realiza la extracción y almacenamiento de datos de noticias de 5 paginas web enfoncadas en ciencia, luego serán consumidas mediante una API por el Front-End.

* revisa el repositorio de la API [aqui](https://github.com/Santiagonk/API_News_Flask).

Mira la documentación del proyecto en Notion:

* [Link Notion](https://www.notion.so/SC-News-P3-C7-dbfdf1278c6d46cb93a342faea648579)


## Requerimientos
------------
Para la instalación necesitas los siquientes requerimientos:

- Python 3
- virtualenv 
- git 

## Instalación
------------
Ejecuta los siguientes comandos:

    $ git clone git@github.com:Santiagonk/Science_News_Scrapy.git
    $ cd Science_News_Scrapy
Crea e inicia el entorno virtual. [Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/#:~:text=Remove%20ads-,What%20Is%20a%20Virtual%20Environment%3F,dependencies%20every%20other%20project%20has.)

    $ pip install scrapy
    
Crea un archivo `.env`, copia la información del archivo `.env.sample` y actualiza con la información de la base de datos en MongoDB que quieres usar.

El proyecto hace uso de 5 Spiders del FrameWork Scrapy, para ejecutar un Spider ub:

    $ cd Scrapy_News
    $ scrapy crawl <Spider_name>
    
Ejemplo:

    $   scrapy crawl nature
    
#### Consideraciones

El proyecto actualmente respeta el Robots.txt, sin embargo antes de ejecutar los comandos revisa las politicas de las paginas.
    
### SCRAPPER VERSION
------------
Version 1.0

### Lenguajes
------------
* Python
* Flask (Framework)

### Base de Datos
------------
* MongoDB

## License

MIT
