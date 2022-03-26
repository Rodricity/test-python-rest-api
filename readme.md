# Django REST HTTP API para usuarios

## Introducción

El presente repositorio contiene la solución al desafío de generar una API HTTP REST para el manejo de usuarios. Por motivos del proceso de selección y dado que el interesado utiliza Django para su sistema de backend se implementó este sistema usando dicho framework; No obstante una solución más minimalista hubiera sido igualmente lograble mediante Flask.

## Descripción de la App

Esta aplicación permite levantar un servidor web capaz de reponder a peticiones HTTP REST para la administración de usuarios en una 'base de datos' almacenada en memoria. Dicha base de datos en realidad no es más que un listado de objetos que son manipulados a través de un controlador y un modelo.

## Puesta en marcha

### Prerequisitos

- Este proyecto fue desarrollado para la versión 3.9 de ptyhon, aunque en general debería funcionar bien con cualquier versión de ptyhon 3+

- Para administrar de una manera más consitente las dependencias este proyeto requiere mantener instalado pipenv en la máquina que ejecute esta aplicación.

### Instalación

Cumplidos ambos requisitos anteriores bastará con ejecutar los comandos:

```
pipenv install
```

### Ejecución

Una vez instaladas las dependencias del proyecto bastará con utilizar el script de administración de Django para iniciar el servidor.

```bash
# Ingresamos al ambiente virtual de Python
pipenv shell

# Lanzamos el servidor web incluido en Django
python manage.py runserver
```

Si todo ha marchado bien, el proyecto indicará que está listo para recibir peticiones en el puerto 8000.

# Endpoints

Puesto que este proyecto implementa una API REST para el manejo de usuarios, solo se ha implementado el endpoint para al manejo de usuarios.

Toda la comunicación desde y hacia el servidor se realiza mediante el envío de data en formato JSON.

## Usuarios

Los endpoint para el manejo de usuarios llevan el prefijo "/user/", por ejemplo para solicitar todos los usuarios se utilizaría un endpoint de la siguiente manera.

```bash
curl -X GET --url "https://127.0.0.1:8000/user/"
```

Por su parte, cada Usuario dentro del sistema posee la siguiente estructura:

```json
{
	"ID": "String: UUID v4",
	"Nombre": "String: nombre del usuario",
	"Apellido": "String: apellido del usuario",
	"Email": "String: el correo electrónico del usuario",
	"FechaNacimiento": "String: Fecha de nacimiento del usuario"
}
```

### **GET: /user/**

### **GET: /user/&lt;user-id&gt;**

Las peticiones GET tienen por objetivo obtener los usuarios (primer caso) o bien obtener un usuario en particular (segundo caso).

**Nota:** Para el caso del listado de usuarios no se ha implementado el paginado; No obstante esto sí debería considerarse en un caso de aplicación real puesto que de lo contrario el listado retornado podría llegar a ser problemático para una única peticion.

### **POST: /user/**

Endpoint para la creación de un usuario; La data enviada al servidor debe incluir la siguiente información:

```json
{
	"Nombre": "String: nombre del usuario",
	"Apellido": "String: apellido del usuario",
	"Email": "String: el correo electrónico del usuario",
	"FechaNacimiento": "String: Fecha de nacimiento del usuario, formato: YYYY-MM-DD"
}
```

Por su parte el servidor entregará devuelta la información completa del usuario (incluyendo el ID auto-generado)

### **UPDATE: /user/&lt;user-id&gt;**

Endpoint para actualizar un usuario; La información enviada debe ser idéntica al endpoint anterior y adicionalmente la ruta de la petición debe indicar el ID del usuario a editar.

El servidor en respuesta entregará la data del usuario actualizada.

### **DELETE: /user/&lt;user-id&gt;**

Endpoint para eliminar un usuario de la 'base de datos'.

## Testing [Linux]

A modo complementario se ha generado un script en bash para realizar una prueba del sistema de manera automática; Esto se puede transformar en un test unitario en Python e incluirlo como parte del proyecto, no obstante para mantener la solución lo más sencilla posible esto se implementó por fuera.

De igual forma en caso de querer verificar su resultado se puede ejecutar:

```bash
bash/test.sh
```

Este script al estar diseñado para bash no funcionará salvo en máquinas que corran alguna distribución de Linux y tengan instalado el programa 'curl'.

# Comentarios finales

## Django SECRET_KEY

Nunca se debería cargar este parámetro en los repositorios; En este caso al ser una respuesta de un desafío es irrelevante; No así en un entorno de producción.

## Entorno de desarrollo

El entorno de desarrollo local ha sido Ubuntu LTS; No debiese haber problemas de utilizar este repositorio en Windows no obstante (a opinión personal) un entorno de desarrollo debería ser lo más similar a un entorno de producción.
