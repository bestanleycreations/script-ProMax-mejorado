import json
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Token y configuración
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 1️⃣ Ruta: Crear columnas faltantes
@app.route("/crear_columnas", methods=["POST"])
def crear_columnas():
    columnas_base = [
        "ID Único Interno", "Nombre Documento", "Tipo de Contenido", "Documento base", "Estado",
        "Función del agente / Doc técnico", "Proyecto", "Plataforma de destino",
        "Escenario Make Relacionado", "Última Modificación", "Agente Responsable",
        "Ruta Carpeta Final", "Nombre Archivo", "Versión Documento", "Notas Adicionales"
    ]
    database_id = os.getenv("NOTION_DATABASE_ID")
    response = requests.get(
        f"https://api.notion.com/v1/databases/{database_id}",
        headers=HEADERS
    )
    db_data = response.json()
    existing_properties = db_data.get("properties", {})
    existing_columns = list(existing_properties.keys())

    resultado = {"creadas": [], "ya_existian": []}
    for columna in columnas_base:
        if columna in existing_columns:
            resultado["ya_existian"].append(columna)
        else:
            nueva_propiedad = {
                "properties": {columna: {"multi_select": {}}}
            }
            requests.patch(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers=HEADERS,
                json=nueva_propiedad
            )
            resultado["creadas"].append(columna)
    return jsonify(resultado), 200

# 2️⃣ Ruta: Actualizar entradas específicas
@app.route("/actualizar_entrada", methods=["PATCH"])
def actualizar_entrada():
    data = request.json
    page_id = data.get("page_id")
    campos = data.get("campos")
    if not page_id or not campos:
        return jsonify({"error": "Faltan 'page_id' o 'campos' en la solicitud."}), 400
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.patch(url, headers=HEADERS, json={"properties": campos})
    if response.status_code == 200:
        return jsonify({"status": "actualizado", "page_id": page_id}), 200
    else:
        return jsonify({"error": response.text}), response.status_code

# 3️⃣ Ruta: Crear etiquetas (standby – se completa más adelante)
@app.route("/crear_etiquetas", methods=["POST"])
def crear_etiquetas():
    return jsonify({"mensaje": "Función crear_etiquetas en preparación."}), 200

# 4️⃣ Ruta: Documentación técnica automática (standby)
@app.route("/crear_documentacion", methods=["POST"])
def crear_documentacion():
    return jsonify({"mensaje": "Función crear_documentacion en preparación."}), 200

# 5️⃣ Ruta: Acciones lógicas condicionales (standby)
@app.route("/acciones_logicas", methods=["POST"])
def acciones_logicas():
    return jsonify({"mensaje": "Función acciones_logicas en preparación."}), 200

# Ejecución del servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
