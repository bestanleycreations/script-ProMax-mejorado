import json
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

@app.route("/crear_columnas", methods=["POST"])
def crear_columnas():
    columnas_base = [
        "ID Único Interno", "Nombre Documento", "Tipo de Contenido", "Documento base", "Estado",
        "Función del agente / Doc técnico", "Proyecto", "Plataforma de destino",
        "Escenario Make Relacionado", "Última Modificación", "Agente Responsable",
        "Ruta Carpeta Final", "Nombre Archivo", "Versión Documento", "Notas Adicionales"
    ]
    response = requests.get(
        f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}",
        headers=HEADERS
    )
    props = response.json().get("properties", {})
    existing = list(props.keys())

    result = {"creadas": [], "ya_existian": []}
    for col in columnas_base:
        if col in existing:
            result["ya_existian"].append(col)
        else:
            patch = {"properties": {col: {"multi_select": {}}}}
            requests.patch(
                f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}",
                headers=HEADERS,
                json=patch
            )
            result["creadas"].append(col)
    return jsonify(result), 200

@app.route("/actualizar_entrada", methods=["PATCH"])
def actualizar_entrada():
    data = request.json
    page_id = data.get("page_id")
    campos = data.get("campos")
    if not page_id or not campos:
        return jsonify({"error": "Faltan 'page_id' o 'campos' en la solicitud."}), 400

    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.patch(url, headers=HEADERS, json={"properties": campos})
    if resp.status_code == 200:
        return jsonify({"status": "actualizado", "page_id": page_id}), 200
    else:
        return jsonify({"error": resp.text}), resp.status_code

@app.route("/crear_etiquetas", methods=["POST"])
def crear_etiquetas():
    data = request.json
    etiquetas = data.get("etiquetas_necesarias", {})
    if not etiquetas:
        return jsonify({"error": "Sin etiquetas en el cuerpo de la solicitud."}), 400

    resp = requests.get(
        f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}",
        headers=HEADERS
    )
    props = resp.json().get("properties", {})

    mensajes = {}
    for campo, lista in etiquetas.items():
        # verifica existencia de la propiedad
        prop = props.get(campo)
        if not prop:
            mensajes[campo] = "Campo no existe"
            continue
        tipo = prop.get("type")
        if tipo not in ["select", "multi_select"]:
            mensajes[campo] = f"Tipo no válido: {tipo}"
            continue

        # Obtener opciones actuales
        opciones = []
        if tipo == "select":
            opciones = prop["select"].get("options", [])
        elif tipo == "multi_select":
            opciones = prop["multi_select"].get("options", [])

        nombres_existentes = [o["name"] for o in opciones]
        nuevas = [x for x in lista if x not in nombres_existentes]
        if nuevas:
            opciones.extend([{"name": x} for x in nuevas])
            update = {"properties": {campo: {tipo: {"options": opciones}}}}
            requests.patch(
                f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}",
                headers=HEADERS,
                json=update
            )
            mensajes[campo] = f"{len(nuevas)} etiquetas creadas"
        else:
            mensajes[campo] = "Sin etiquetas nuevas"

    return jsonify({"resultado": mensajes}), 200

@app.route("/crear_documentacion", methods=["POST"])
def crear_documentacion():
    return jsonify({"mensaje": "Función crear_documentacion en preparación."}), 200

@app.route("/acciones_logicas", methods=["POST"])
def acciones_logicas():
    return jsonify({"mensaje": "Función acciones_logicas en preparación."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
