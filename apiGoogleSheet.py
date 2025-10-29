from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
import gspread
from google.oauth2.service_account import Credentials
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
    


@app.post("/sheets/sync")
def sync_sheets_to_mysql():
    conn = None
    cursor = None
    try:
        # Leer la URL del archivo sheetRequest.json
        with open("sheetRequest.json", "r") as f:
            data = json.load(f)

        url = data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="No se encontró 'url' en sheetRequest.json")

        # Abrir la hoja de Google Sheets
        sh = gc.open_by_url(url)
        worksheet = sh.sheet1
        rows = worksheet.get_all_records()

        conn = get_connection()
        cursor = conn.cursor()

        registros_insertados = 0

        
        for row in rows:
            fecha = row.get("Marca temporal", "")
            espacio = row.get("Espacio Curricular", "")
            docente = row.get("Docente", "")

            
            for pregunta, respuesta in row.items():
                if pregunta in ["Marca temporal", "Espacio Curricular", "Docente"]:
                    continue 

                sql = """
                    INSERT INTO RespuestasDeGoogle (respuesta, fecha, pregunta, espacio_curricular, docente)
                    VALUES (%s, %s, %s, %s, %s)
                """
                valores = (str(respuesta), fecha, pregunta, espacio, docente)
                cursor.execute(sql, valores)
                registros_insertados += 1

        conn.commit()

        return {
            "status": "OK",
            "mensaje": f"Migración completada con éxito. {registros_insertados} registros insertados."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


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


