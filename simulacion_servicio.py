import requests
import json
import time
import random
from datetime import datetime

# Generamos logs aleatorios
def generar_log(nombre_servicio):
    nivel = ["INFO", "ERROR", "DEBUG"]
    log = {
        "nombre_servicio": nombre_servicio,
        "nivel": random.choice(nivel),
        "fecha_hora": datetime.now().isoformat(),  # Llamar al método con paréntesis
        "mensaje": "Se ha generado un log"
    }
    return log

# Enviamos el log aleatorio al servidor central
def enviar_log(log, url, token):
    encabezado = {
        # Enviar un token de autenticación
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, data=json.dumps(log), headers=encabezado)  # Corregir 'encabezado' a 'headers'
    return response.status_code

# URL del servidor central
server_url = "http://localhost:5000/logs"

# Token de autenticación
token = "token_de_servicio"

# Simulación del servicio generando y enviando logs
nombre_servicio = "Servicio A"
while True:
    log = generar_log(nombre_servicio)
    status_code = enviar_log(log, server_url, token)
    print(f"Status code: {status_code}")
    time.sleep(5)  # Esperamos 5 segundos antes de generar otro log
