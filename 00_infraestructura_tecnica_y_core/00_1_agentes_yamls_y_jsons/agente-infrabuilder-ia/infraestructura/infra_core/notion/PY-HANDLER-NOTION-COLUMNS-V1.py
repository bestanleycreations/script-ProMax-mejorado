import json

json_estructura = {
    "estructura": {
        "columnas_base": [
            "ID Único Interno",
            "Nombre Documento",
            "Tipo de Contenido",
            "Documento base",
            "Estado",
            "Función del agente / Doc técnico",
            "Proyecto",
            "Plataforma de destino",
            "Escenario Make Relacionado",
            "Última Modificación",
            "Agente Responsable",
            "Ruta Carpeta Final",
            "Nombre Archivo",
            "Versión Documento",
            "Notas Adicionales"
        ]
    }
}

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

COLUMNS_BASE = json_estructura["estructura"]["columnas_base"]

@app.route("/crear_columnas", methods=["POST"])
def crear_columnas():
    response = requests.get(
        f"https://api.notion.com/v1/databases/{DATABASE_ID}",
        headers=HEADERS
    )
    db_data = response.json()
    existing_properties = db_data.get("properties", {})
    existing_columns = list(existing_properties.keys())

    resultado = {
        "creadas": [],
        "ya_existian": []
    }

    for columna in COLUMNS_BASE:
        if columna in existing_columns:
            resultado["ya_existian"].append(columna)
        else:
            nueva_propiedad = {
                "properties": {
                    columna: {
                        "multi_select": {}
                    }
                }
            }
            requests.patch(
                f"https://api.notion.com/v1/databases/{DATABASE_ID}",
                headers=HEADERS,
                json=nueva_propiedad
            )
            resultado["creadas"].append(columna)

    return jsonify(resultado), 200

if __name__ == "__main__":
    app.run(debug=True)
