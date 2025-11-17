from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
import gspread
from google.oauth2.service_account import Credentials
import json




conDB = {
    "host": "localhost",
    "user": "jesica_Suarez",
    "password": "Matucana5276",
    "database": "Google_Form_To_MySQL"
}

scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
credenciales = "credenciales.json"

credentials = Credentials.from_service_account_file(credenciales, scopes=scope)
gc = gspread.authorize(credentials)

app = FastAPI(
    title="GoogleSheet To MySQL",
    description="API Migración de datos de múltiples GoogleSheets a MySQL",
    version="1.0.0"
)


def get_connection():
    """Abrir conexión MySQL"""
    return mysql.connector.connect(**conDB)


@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API GoogleSheet + MySQL "}
    

@app.post("/sheets/sync")
def sync_sheets_to_mysql():
    conn = None
    cursor = None

    try:
        # Lee el archivo JSON
        with open("sheetRequest.json", "r") as f:
            data = json.load(f)

        urls = data.get("url")

        if not urls:
            raise HTTPException(status_code=400, detail="No se encontró 'url' en sheetRequest.json")

        
        if isinstance(urls, str):
            urls = [urls]

        conn = get_connection()
        cursor = conn.cursor()

        registros_insertados = 0
        encuestado = 0

        
        # Recorre cada formulario de Google Sheet del JSON
        
        for url in urls:

            sh = gc.open_by_url(url)
            worksheet = sh.sheet1
            rows = worksheet.get_all_records()

            
            for index, row in enumerate(rows, start=2):
                encuestado += 1

                fecha = row.get("Marca temporal", "")
                espacio = row.get("Espacio Curricular", "")
                docente = row.get("Docente", "")

                try:
                    for pregunta, respuesta in row.items():

                        
                        if pregunta in ["Marca temporal", "Espacio Curricular", "Docente"]:
                            continue

                        sql = """
                            INSERT INTO RespuestasDeGoogle 
                            (respuesta, fecha, pregunta, espacio_curricular, docente, encuestado)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """

                        valores = (str(respuesta), fecha, pregunta, espacio, docente, encuestado)
                        cursor.execute(sql, valores)
                        registros_insertados += 1

                except Exception as e:
                    return {
                        "error": str(e),
                        "sheet_url": url,
                        "fila_google_sheet": index,
                        "contenido_fila": row,
                        "encuestado_actual": encuestado,
                        "registros_insertados_hasta_el_error": registros_insertados
                    }

        conn.commit()

        return {
            "status": "OK",
            "mensaje": "Migración completada desde todos los Google Sheets",
            "total_insertados": registros_insertados,
            "total_encuestados": encuestado
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
        cursor.execute("SELECT * FROM RespuestasDeGoogle")
        return cursor.fetchall()
    except Error as e:
        return {"error": str(e)}
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


