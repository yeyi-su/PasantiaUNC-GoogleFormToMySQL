Pasantias UNC - Migración Google Form a MySQl
Descripción
Proyecto desarrollado durante mi pasantía en la Universidad Nacional de Córdoba (Facultad de Ciencias Agropecuarias).
Con el objetivo desarrollar una solución automatizada para la migración de respuestas provenientes de múltiples formularios de Google Forms hacia una base de datos MySQL. La iniciativa surgió ante la necesidad de centralizar y almacenar de manera estructurada los datos recopilados mediante Google Sheets, permitiendo así un análisis más eficiente y persistente de la información.

Funcionalidades
- Conexión a base de datos MySQL
- Procesamiento de datos obtenidos desde Google Forms
- Inserción automatizada en tablas relacionales
- Validación básica de datos

Tecnologías Utilizadas
- Python
- MySQL
- Librerías de conexión a base de datos
- API REST

INSTRUCCIONES DE USO

#Ejecución de la API

Para ejecutar la API debmos ingresar al directorio donde se encuentra el archivo con el siguiente comando
cd nombre_directorio
Para levantar el servidor (uvicorn nombre_de_archivo:app --reload)
uvicorn apiGoogleSheet:app --reload
Ingresar a localhost:8000/docs

#MySQL
En este caso se utiliza PHPMyAdmin para utilizar la base de datos creada en dicho sitio
Para levantar el servidor de PHPMyAdmin
sudo /opt/lampp/lampp start
Para desactivar el servidor
sudo /opt/lampp/lampp stop
