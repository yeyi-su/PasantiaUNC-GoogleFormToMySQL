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
