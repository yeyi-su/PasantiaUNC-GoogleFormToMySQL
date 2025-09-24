from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error
import gspread
from google.oauth2.service_account import Credentials


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

# -----> Obtener todas las respuestas desde MySQL
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

@app.get("/sheets/respuestas")
def get_sheets_respuestas():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1-Mm50QGdItzI1MHCLmUoz8H87JbunUsJ6RGm7ezCjug/edit"
        sh = gc.open_by_url(sheet_url)   
        worksheet = sh.sheet1
        data = worksheet.get_all_records()
        return data
    except Exception as e:
        return {"error": str(e)}

