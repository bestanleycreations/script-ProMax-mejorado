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

@app.route("/actualizar_entrada", methods=["PATCH"])
def actualizar_entrada():
    data = request.json
    page_id = data.get("page_id")
    campos = data.get("campos")

    if not page_id or not campos:
        return jsonify({"error": "Faltan 'page_id' o 'campos' en el cuerpo de la solicitud."}), 400

    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": campos
    }

    response = requests.patch(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return jsonify({"status": "actualizado", "page_id": page_id, "modificaciones": campos}), 200
    else:
        return jsonify({"status": "error", "code": response.status_code, "detalle": response.text}), response.status_code

# Ejecución del servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
