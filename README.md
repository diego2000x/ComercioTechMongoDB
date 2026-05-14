# ComercioTechMongoDB
App de terminal que gestiona la base de datos de la tienda ficticia ComercioTech

## Requisitos
- Docker Desktop instalado
- Los datos de ejemplo para testear la app deben cargarse antes de usar la app, las 4 colecciones estan incluidas en un JSON para cada una.

## Cómo ejecutar
1. Clonar el repositorio
2. Abrir una terminal en la carpeta del proyecto
3. Ejecutar:
   docker compose up --build
4. Para usar la app:
   docker compose run app

## Notas
- Iniciar.bat es solo para pruebas de desarrollo y ejecuta MongoDB y la App Python en Docker ademas de mostrar instantaneamnete un terminal con la app, para funcionar los nombres de los contenedores en Docker deben ser los correctos (mongodb y comerciotech).
