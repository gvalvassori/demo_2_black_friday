# <h1 align=center>**`Data Science - Demo Black Friday`**</h1>

En este repositorio podrán observar el contenido de los archivos utilizados para el desarrollo del modelo predictivo ***Black friday***.

## **Pasos del proceso**

1. Se trabaja con Notebooks de diseño y desarrollo que contienen los experimentos realizados desde la fase del análisis exploratorio de datos, el procesamiento de datos e ingeniería de variables, el diseño y entrenamiento de los modelos y la validación de resultados obtenidos, entre otros. Estos Notebooks son utilizados en un contexto de desarrollo y son implementados a través de las instancias de VertexAI Workbench.

2. Una vez obtenido una nueva versión u optimización se procede a la implementación de CI/CD a través de lógica basada en el framework Kubeflow junto con la integración de los servicios de canalizaciones dentro del entorno de Vertex AI. A partir de componentes que integran un flujo de datos dentro de la creación de un pipeline se debe optimizar el desarrollo realizado en este tipo de canalización para ser registrado como una plantilla ejecutable dentro del entorno de Vertex AI - Canalizaciones.

3. Se diseñó una lógica a partir de la integración de Cloud Build activando un trigger que escucha los cambios subidos al repositorio de Cloud Source Repositories. Este trigger al detectar un commit ejecuta el archivo cloudbuild.yaml, el cual contiene la configuración con las instrucciones para Cloud Build. Este flujo de trabajo automatiza la configuración del entorno Python (instalación de dependencias requirements.txt) para luego relizar la ejecución del script principal main.py, el cual contiene la lógica para compilar la canalización descrita, registrar esta misma como un artefacto dentro de Artifact Registry y crear la programación de la ejecución mensual de esta misma canalización.

## **Aclaraciones**

+ La carpeta "notebooks" contiene los archivos Jupyter Notebooks que se desarrollaron para las fases contempladas en la creación del modelo predictivo. Contemplando desde el EDA hasta la generación de componentes para construir una canalización.

+ La carpeta "reports" contiene los archivos PDF donde se describen los resultados de la fase EDA y los resultados del modelo final.

+ La carpeta "src/components" contiene los modulos de python que construyen los componentes para cada paso del DAG que se define en **pipeline.py**.

+ **src/pipeline.py:** En este se construye la canalización definiendo los argumentos de entrada y salida tanto para el DAG como para cada uno de sus componentes.

+ **src/main.py:** contiene todo el proceso de obtención de información de pipelines y el despliegue de los mismos.

+ **cloudbuild.yaml:** El archivo cloudbuild.yaml es un archivo de configuración de compilación que contiene instrucciones para Cloud Build. Este flujo de trabajo de construcción automatiza la configuración del entorno Python, la instalación de dependencias y la ejecución de scripts principales (main_df.py y main_sp.py).

+ **requirements.txt:** define las dependencias necesarias para ejecutar correctamente el archivo main_df.py.


## Code origin certification

Todos los códigos utilizados fuero desarrollados por CoreBI S.A., la parte de MLOps fue desarrollada haciendo uso de la documentación oficial de Kubeflow y su adaptación de Google

* [Build a pipeline](https://cloud.google.com/vertex-ai/docs/pipelines/build-pipeline)

Todos los componentes utilizados son open source.
