# ST02363 Tópicos Especiales en Telemática

# Estudiante: Alejandro Torres Muñoz, eatorresm@eafit.edu.co

# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co


# Reto 2


# 1. breve descripción de la actividad
Para este reto, se implementaron 3 microservicios:

- **Microservicio 1:** Encargado de listar archivos a través de gRPC. Se comunica con el API Gateway.

- **Microservicio 2:** Encargado de buscar archivos mediante una query a través de MOM (RabbitMQ). Se comunica con el API Gateway.

- **Microservicio API Gateway:** Encargado de funcionar tanto como gateway como balanceador de cargas y proxy.
  

## 1.1. Qué aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- Implementación de microservicio 1.

- Implementación de microservicio 2.

- Implementación de microservicio API Gateway.

- Comunicación vía gRPC para el microservicio 1.

- Comunicación vía MOM (RabbitMQ) para el microservicio 2.

- Comunicación API Rest entre cliente y API Gateway.

- Archivos de configuración dinámicos.

- Implementación de endpoints tanto para listar archivos como para buscar.

- Concurrencia para cada microservicio.


## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Todos los requerimientos fueron implementados.

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

! [Arquitectura](./Arquitectura.png)

Podemos observar 4 componentes fundamentales para el desarrollo y la arquitectura del proyecto:

**1. API Gateway.
2. Microservicio 1.
3. MOM (RabbitMQ).
4. Microservicio 2.**

El cliente hace una petición sea a través de su navegador web, o desde Postman. Éste se comunica mediante API Rest. El API Gateway a su vez se comunica mediante gRPC con el primer microservicio, el cual es el encargado de listar archivos. El segundo microservicio es mediante comunicación MOM, utilizando RabbitMQ. Este funciona con colas y es el encargado de buscar archivos a través de una query que el usuario pasa. Dependiendo del tipo de solicitud que se haga se toma una comunicación u otra.

- Se utilizó Python como lenguaje de programación.
- Se utilizó Docker como orquestador del sistema.
- Como buenas prácticas se hace uso de variables de entorno, métodos desacoplados y directorios bien distribuidos.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

Todos los servicios fueron implementados con Python 3.10.6. En el proyecto, encontrará un archivo llamado "requirements.txt", donde se especifican la lista de bibliotecas utilizadas.

    Flask==2.2.3
    grpc==1.0.0
    grpcio==1.51.3
    pika==1.3.1
    protobuf==4.22.0
    python-dotenv==1.0.0

Flask se utilizó para implementar la puerta de enlace API, grpcio es la biblioteca del kit de herramientas gRPC para implementar el microservicio 1 y pika es la biblioteca de cliente RabbitMQ para implementar el microservicio 2.

## como se compila y ejecuta.

PENDIENTE

## detalles del desarrollo.

Se implementó como primera instancia, el microservicio 1, este permite consultar los archivos mediante una comunicación gRPC. Luego de tener funcionando este microservicio, se procede a utilizar Flask como API Gateway. Finalmente se implementa el microservicio 2, el cual permite buscar los archivos mediante una query, y se comunica mediante MOM, precisamente con RabbitMQ.

- Proyecto desarrollado en Python.
- Se orquestó mediante Docker.
- Se utilizó Git como versión de controles.
- Se desplegó en una máquina virtual de AWS.

## detalles técnicos

- **Arquitectura:** Microservicios.
- **Comunicacion entre microservicios:** gRPC y RabbitMQ.
- **Plataforma y servicios en nube:** Amazon AWS (EC2 Ubuntu, IPs elásticas)
- **Orquestación del proyecto:** Docker

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)



PENDIENTE



## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)

PENDIENTE

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

 Aplica el mismo lenguaje, librerías, paquetes y demás, utilizados en ambiente de desarrollo.

# IP o nombres de dominio en nube o en la máquina servidor.

  PENDIENTE 

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

  PENDIENTE

## como se lanza el servidor.

PENDIENTE  

## una mini guia de como un usuario utilizaría el software o la aplicación

  PENDIENTE 

## opcionalmente - si quiere mostrar resultados o pantallazos

  PENDIENTE 

# referencias:

  - https://grpc.io/docs/what-is-grpc/introduction/
  - https://grpc.io/docs/languages/python/basics/
  - https://www.rabbitmq.com/tutorials/tutorial-six-python.html
  - https://flask.palletsprojects.com/en/2.2.x/quickstart/

#### versión README.md -> 1.0 (2022-agosto)
