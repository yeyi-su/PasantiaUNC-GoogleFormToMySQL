#Pasantias UNC - Migración Google Form a MySQL
##Descripción
Proyecto desarrollado durante mi pasantía en la Universidad Nacional de Córdoba (Facultad de Ciencias Agropecuarias).
Con el objetivo desarrollar una solución automatizada para la migración de respuestas provenientes de múltiples formularios de Google Forms hacia una base de datos MySQL. La iniciativa surgió ante la necesidad de centralizar y almacenar de manera estructurada los datos recopilados mediante Google Sheets, permitiendo así un análisis más eficiente y persistente de la información.

##Funcionalidades
- Conexión a base de datos MySQL
- Procesamiento de datos obtenidos desde Google Forms
- Inserción automatizada en tablas relacionales
- Validación básica de datos

##Tecnologías Utilizadas
- Python
- FastAPI
- Uvicorn
- MySQL
- PHPMyAdmin (para administración de base de datos)
- Credenciales de Google

#INSTRUCCIONES DE USO

1 Ejecución de la API

Para ejecutar la API debemos ingresar al directorio donde se encuentra el archivo con el siguiente comando
'''bash cd nombre_directorio
Para levantar el servidor (uvicorn nombre_de_archivo:app --reload)
'''bash uvicorn apiGoogleSheet:app --reload
Ingresar a localhost:8000/docs

2 MySQL
En este caso se utiliza PHPMyAdmin para utilizar la base de datos creada en dicho sitio
Para levantar el servidor de PHPMyAdmin
'''bash sudo /opt/lampp/lampp start
Para desactivar el servidor
'''bash sudo /opt/lampp/lampp stop
