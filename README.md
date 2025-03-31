SpaceX Data Processor
=====================

Descripción
-----------

SpaceX Data Processor es una aplicación diseñada para recopilar, procesar y visualizar datos de los lanzamientos de SpaceX. Utiliza AWS Lambda, DynamoDB y una interfaz web en Docker para gestionar y mostrar la información de manera eficiente.

Características
---------------

*   **Procesamiento de datos:** Función Lambda para procesar datos de SpaceX.
    
*   **Almacenamiento en DynamoDB:** Base de datos NoSQL para gestionar los registros de los lanzamientos.
    
*   **Interfaz gráfica:** Aplicación web desarrollada en Python con Flask.
    
*   **Despliegue local con LocalStack:** Simulación de los servicios AWS en entorno local.
    
*   **Integración con Docker:** Contenedor para facilitar la ejecución de la aplicación.
    

Requisitos Previos
------------------

Antes de ejecutar la aplicación, asegúrate de tener instalados los siguientes componentes:

### Instalación de Dependencias

1.  **Docker y Docker Compose** ([Descargar Docker](https://www.docker.com/get-started))
    
2.  **AWS CLI** ([Instalar AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html))

3.  **LocalStackCLI** ([Instalar LocalStack CLI](https://docs.localstack.cloud/getting-started/installation/))
   
4.  Crear y ejecutar LocalStack  
 ```sh
docker run --rm -it -p 4566:4566 -p 4571:4571 -v /var/run/docker.sock:/var/run/docker.sock localstack/localstack
  ```

5.  **Python 3.8 o superior** ([Descargar Python](https://www.python.org/downloads/))
    
6. **Instalar dependencias**
```sh
pip install -r dependencies.txt
```    

Tecnologías Utilizadas
----------------------

### Lenguajes y Frameworks

*   **Python 3.8**
    
*   **Flask (para la interfaz web)**
    
*   **Boto3 (para interacción con AWS)**
    

### Herramientas y Servicios

*   **AWS Lambda** (para procesar datos)
    
*   **Amazon DynamoDB** (para almacenamiento de información)
    
*   **LocalStack** (para emular servicios de AWS en local)
    
*   **Docker** (para contenedorización de la aplicación)
    
*   **GitHub Actions** (para integración continua y despliegue)
    

Ejecución
---------

Para ejecutar la aplicación, sigue los pasos descritos en la documentación detallada del proyecto. Esto incluye la configuración de LocalStack, despliegue de los stacks de AWS, configuración de Lambda y ejecución del contenedor Docker para visualizar la interfaz gráfica.

Para más detalles, revisa la guía de instalación y despliegue en la documentación del repositorio ([Documentación Ejecucion de Aplicación](https://docs.google.com/document/d/15HVSdgozz9WJxmQMahgvOOiPcc46tiCwNib41-VF0E0/edit?tab=t.0)).

