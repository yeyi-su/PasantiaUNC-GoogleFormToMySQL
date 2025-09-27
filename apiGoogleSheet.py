from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
import gspread
from google.oauth2.service_account import Credentials
from pydantic import BaseModel
import json


#Coneccion Base de Datos

conDB = {

	"host":"localhost",
	"user":"jesica_Suarez",
	"password":"Matucana5276",
	"database":"Google_Form_To_MySQL"
}

scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

sheet = "Test Administración de la Empresa Agropecuaria - Federico Ceccon  (respuestas)"

credenciales = "credenciales.json"

credentials = Credentials.from_service_account_file(credenciales, scopes=scope)
gc = gspread.authorize(credentials)

app = FastAPI(
    title="GoogleSheet To MySQL",
    description="API Migración de datos de GoogleSheet a una base de datos MySQL",
    version="1.0.0"
)


def get_connection():
    """Abrir conexión MySQL"""
    return mysql.connector.connect(**conDB)


# Enpoints


@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API GoogleSheet + MySQL "}
    


@app.post("/sheets/respuestas")
def get_sheets_respuestas():
    try:
        # Abrir el archivo JSON con UNA sola URL
        with open("sheetRequest.json", "r") as f:
            data = json.load(f)

        url = data.get("url")

        if not url:
            raise HTTPException(status_code=400, detail="No se encontró 'url' en sheetRequest.json")

        # Conectarse a Google Sheet
        sh = gc.open_by_url(url)
        worksheet = sh.sheet1
        respuestas = worksheet.get_all_records()

        return {url: respuestas}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/mysql/respuestas")
def get_mysql_respuestas():
	conn = None
	cursor = None
	try:
		conn = get_connection()
		cursor = conn.cursor(dictionary=True)
		cursor.execute("SELECT * FROM RespuestasDeFormGoogle")
		return cursor.fetchall()
	except Error as e:
		return {"error": str(e)}
	finally:
		if cursor is not None:
			cursor.close()
		if conn is not None:
			conn.close()


