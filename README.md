# CookGen-API

Una API que genera recetas de cocina personalizadas según los ingredientes disponibles y las preferencias alimentarias.

## Tabla de Contenidos

- [Descripcion del Repositorio](#descripcion-del-repositorio)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Endpoints](#endpoints)
- [Configuracion Inicial](#configuracion-inicial)
- [Testing](#testing)
- [Code Style y Normas](#code-style-y-normas)

## Descripcion del Repositorio

Este repositorio contiene una aplicación FastAPI que permite a los usuarios generar recetas de cocina basadas en ingredientes disponibles y preferencias alimentarias. La aplicación ofrece funcionalidades de autenticación, gestión de usuarios, recetas e ingredientes.

## Estructura del Proyecto

- **alembic**: Contiene archivos relacionados con las migraciones de la base de datos.
  - **versions**: Scripts específicos de migración para actualizar la base de datos.
  
- **app**: Directorio principal de la aplicación.
  - **auth**: Módulo para autenticación, incluyendo rutas, esquemas y utilidades.
  - **ingredients**: Módulo para gestionar ingredientes.
  - **recipes**: Módulo para gestionar recetas.
  - **users**: Módulo para gestionar usuarios.
  - **static**: Contiene archivos estáticos como imágenes y CSVs.
  - **main.py**: Punto de entrada principal de la aplicación.
  - **models.py**: Define los modelos de la base de datos.
  - **schemas.py**: Esquemas Pydantic para validación y serialización.
  - **database.py**: Configuración y conexión a la base de datos.
  - **config.py**: Configuraciones generales de la aplicación.
  - **init_data.py**: Script para inicializar datos en la base de datos.

- **docker-compose.yml**: Define y configura los servicios de Docker.
- **Dockerfile**: Instrucciones para construir la imagen Docker de la aplicación.
- **Makefile**: Comandos útiles para gestionar y desplegar la aplicación.
- **requirements.txt**: Lista de dependencias del proyecto.
- **tests**: Contiene pruebas unitarias para los diferentes módulos de la aplicación.

## Endpoints

### Módulo de Auth:
- `POST /auth/register`: Registrar un nuevo usuario.
- `POST /auth/login`: Iniciar sesión (Obtiene un JWT Token).
- `GET /auth/verify`: Verifica un JWT Token.
- `POST /auth/logout`: Revoca un token por el tiempo de vida que le queda.

### Módulo de Usuarios:
- `GET /users/me`: Obtener información del usuario actual.
- `GET /users/me/preferences`: Obtiene las preferencias del usuario.
- `POST /users/me/preferences`: Crea o Actualiza una preferencia del usuario.
- `POST /users/me/saved-recipes`: Guardar una receta generada.
- `GET /users/me/saved-recipes`: Ver todas las recetas guardadas.
- `DELETE /users/me/saved-recipes/{recipe_id}`: Eliminar una receta guardada.

### Módulo de Recetas:
- `GET /recipes`: Listar todas las recetas.
- `POST /recipes`: Crear una nueva receta.
- `GET /recipes/{recipe_id}`: Obtener detalles de una receta específica.
- `PUT /recipes/{recipe_id}`: Actualizar una receta específica.
- `DELETE /recipes/{recipe_id}`: Eliminar una receta específica.
- `POST /recipes/{recipe_id}/image`: Subir/Actualizar imagen de una receta.
- `GET /recipes/generate`: Devuelve una lista de recetas basadas en las preferencias del usuario.

### Módulo de Ingredientes:
- `GET /ingredients`: Listar todos los ingredientes disponibles.
- `POST /ingredients`: Añadir un nuevo ingrediente.
- `PUT /ingredients/{ingredient_id}`: Actualizar un ingrediente.
- `DELETE /ingredients/{ingredient_id}`: Eliminar un ingrediente.

## Configuracion Inicial
1. Clona este repositorio:
```bash
git clone https://github.com/Xukay101/CookGen-API.git
```
2. Compile, inicie los contenedores Docker, aplique migraciones de bases de datos e inicialice datos:
```bash
make build
```

## Testing
Para ejecutar las pruebas dentro del contenedor Docker, ejecute:
``` bash
make tests
```
Después de configurar con `make build`, puede ejecutar las pruebas. Es importante asegurarse de que la aplicación se construye primero para que las pruebas funcionen correctamente.

## Code Style y Normas
Este proyecto se adhiere a las convenciones de codificación estándar de Python y a las mejores prácticas de FastAPI.

## Tecnologías Utilizadas

- FastAPI
- Docker
- Alembic (para migraciones de base de datos)
- Mysql
- Redis (para el cache de la aplicacion)