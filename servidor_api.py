from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
db_ruta = "api_logs_mania.db"

# Creación de la base de datos y la tabla logs
def crear_db():
    with sqlite3.connect(db_ruta) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_servicio VARCHAR(150),
        nivel TEXT,
        fecha_hora DATE,
        mensaje VARCHAR(255),
        recibido TEXT
        )
        """)
    print("Inicializando la Base Datos")

# Verificar el token de autenticación
def verificar_token(token):
    tokens_validos = ["token_de_servicio"]
    return token in tokens_validos

@app.route("/logs", methods=["POST"])
def recibir_log():
    token = request.headers.get("Authorization", "").split("Bearer ")[-1]
    if not verificar_token(token):
        return jsonify({"error": "Token Invalido"}), 401
    
    log = request.get_json()
    log["recibido"] = datetime.now().isoformat()

    with sqlite3.connect(db_ruta) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (nombre_servicio, nivel, fecha_hora, mensaje, recibido)
            VALUES (:nombre_servicio, :nivel, :fecha_hora, :mensaje, :recibido)
        """, log)
    return jsonify({"status": "Log Recibido"}), 201

@app.route("/logs", methods=["GET"])
def obtener_logs():
    parametros = request.args
    fecha_inicio = parametros.get("fecha_inicio")
    fecha_finalizacion = parametros.get("fecha_finalizacion")

    query = "SELECT * FROM logs WHERE 1=1"
    params = {}
    if fecha_inicio:
        query += " AND fecha_hora >= :fecha_inicio"
        params['fecha_inicio'] = fecha_inicio
    if fecha_finalizacion:
        query += " AND fecha_hora <= :fecha_finalizacion"
        params['fecha_finalizacion'] = fecha_finalizacion
    
    with sqlite3.connect(db_ruta) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        logs = cursor.fetchall()
    return jsonify({"logs": logs}), 200

if __name__ == "__main__":
    if not os.path.exists(db_ruta):
        crear_db()
    app.run(debug=True)
