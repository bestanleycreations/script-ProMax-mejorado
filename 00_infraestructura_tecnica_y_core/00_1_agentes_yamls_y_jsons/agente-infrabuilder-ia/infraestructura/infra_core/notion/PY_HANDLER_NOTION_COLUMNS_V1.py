import json
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Mapeo detallado de columnas con tipo y opciones
COLUMN_CONFIG = {
    "Nombre Documento": {"type": "title"},
    "Fecha Creacion": {"type": "date"},
    "ID Único Interno (Auto)": {"type": "formula"},
    "Tipo de Contenido": {
        "type": "select",
        "options": ["Otro", "post", "video", "diseño", "script", "inicializacion", "Agente GPT / Instrucción técnica /", "Narrativa / Storytelling / Campañas", "Automatización / Estructura técnica / Control del sistema", "Creativo / Generativo / Coordinación estratégica", "Ejecutivo / Estratégico / Supervisor global", "Audiovisual / Técnico / Automatización IA"]
    },
    "Agentes relacionados": {
        "type": "multi_select",
        "options": ["Infra Builder IA", "Agente Video Pipeline Master", "Agente Gemini Pro Max", "Prompt Engineering Pro Max", "Agente de Guiones y Storytelling Creativo Pro Max", "Agente C2 – Cerebro Técnico / Estratégico"]
    },
    "Documento base": {"type": "rich_text"},
    "Estado": {
        "type": "status",
        "options": {
            "options": [
                {"name": "Pendiente", "color": "red"},
                {"name": "En progreso", "color": "yellow"},
                {"name": "Completado", "color": "green"}
            ]
        }
    },
    "Estado de publicacion": {
        "type": "select",
        "options": ["Publicado", "En revision", "Rechazado", "Borrador"]
    },
    "Función Técnica / Descripción Operativa": {"type": "rich_text"},
    "ID Único Registro": {
        "type": "multi_select",
        "options": ["AG-MUSIC-ID-V1", "AG-INFRA-BC-2025-V1", "AG-GEMINIPROMAX-BC-2025-V1.1"]
    },
    "Notas Internas": {"type": "rich_text"},
    "Prioridad Automatica": {
        "type": "select",
        "options": ["Baja", "Media", "Alta", "Maxima"]
    },
    "Ultima Actualizacion": {"type": "date"},
    "URL del Contenido/Producto": {"type": "url"},
    "Proyecto": {
        "type": "multi_select",
        "options": ["Prology by Bestanley", "Bestanleycreations", "Bestanley Universe"]
    },
    "Tipo de Producto": {
        "type": "multi_select",
        "options": ["E-book", "Paquete digital", "Narrativa", "Stickers", "Audiolibro", "Video serie"]
    },
    "Edad Recomendada": {
        "type": "select",
        "options": ["0-3 años", "3-5 años", "7-10 años", "Adultos"]
    },
    "Trazabilidad automática": {
        "type": "multi_select",
        "options": ["Auto-Publicado", "Auto-Revisado", "Auto-Bloqueado"]
    },
    "Estrategia de versión y originalidad": {
        "type": "multi_select",
        "options": ["Versión A original", "Contenido 100% original", "Requiere rediseño"]
    },
    "Plataforma de Destino": {
        "type": "multi_select",
        "options": ["Etsy", "Shopify", "YouTube - Series", "Instagram", "Pinterest"]
    },
    "Palabras Clave / Tags": {"type": "rich_text"},
    "Precio de Venta": {"type": "number"},
    "Categoría Principal": {"type": "multi_select"},
    "Archivo Digital (Descarga)": {"type": "files"},
    "Diseño para Proveedor (POD)": {"type": "files"},
    "Imágenes de Promoción": {"type": "files"},
    "Material de Archivo / Origen": {"type": "files"},
    "Contenido Final (Capítulos/Lotes)": {"type": "files"},
    "Estado operativo documento": {
        "type": "select",
        "options": ["Activo", "No activo"]
    }
}

@app.route("/crear_columnas", methods=["POST"])
def crear_columnas():
    response = requests.get(
        f"https://api.notion.com/v1/databases/{DATABASE_ID}",
        headers=HEADERS
    )
    db_data = response.json()
    existing_properties = db_data.get("properties", {})
    existing_columns = list(existing_properties.keys())

    resultado = {"creadas": [], "ya_existian": []}

    for nombre_columna, config in COLUMN_CONFIG.items():
        if nombre_columna in existing_columns:
            resultado["ya_existian"].append(nombre_columna)
            continue

        nueva_propiedad = {"properties": {nombre_columna: {}}}
        tipo = config["type"]

        if tipo == "select" or tipo == "multi_select":
            nueva_propiedad["properties"][nombre_columna][tipo] = {
                "options": [{"name": tag} for tag in config.get("options", [])]
            }
        elif tipo == "status":
            nueva_propiedad["properties"][nombre_columna]["status"] = config["options"]
        elif tipo == "files":
            nueva_propiedad["properties"][nombre_columna]["files"] = {}
        else:
            nueva_propiedad["properties"][nombre_columna][tipo] = {}

        requests.patch(
            f"https://api.notion.com/v1/databases/{DATABASE_ID}",
            headers=HEADERS,
            json=nueva_propiedad
        )
        resultado["creadas"].append(nombre_columna)

    return jsonify(resultado), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
