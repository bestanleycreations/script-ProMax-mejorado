# handler_hub_promax.py
# Sistema ProMax – Handler Centralizado (HUB)
# Autor: Stanley (BestanleyCreations)
# Fecha: 2025-08-02
# Descripción: Handler Flask para gestión inteligente de documentación técnica y agentes IA en Notion/GitHub

from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Simulación de base de datos interna (para demo, luego reemplazar con acceso real a Notion, GitHub, etc.)
notion_data = {}
github_files = {}

# --- UTILIDADES ---
def get_existing_document(doc_id):
    return notion_data.get(doc_id)

def check_if_manual_entry(doc_data):
    return doc_data.get("origen") == "manual"

def validate_essential_fields(doc_data):
    return all([doc_data.get(k) for k in ["rol", "contexto", "instrucciones"]])

def log_action(doc_id, action, origen="handler_hub", detalle=None):
    log = notion_data[doc_id].setdefault("historial_acciones", [])
    log.append({
        "fecha": datetime.now().isoformat(),
        "accion": action,
        "origen": origen,
        "detalle": detalle or {}
    })

def is_duplicate(new_doc):
    for doc in notion_data.values():
        if doc.get("nombre") == new_doc.get("nombre") and doc.get("id") != new_doc.get("id"):
            return True
    return False

# --- ENDPOINT PRINCIPAL ---
@app.route("/hub_handler", methods=["POST", "PATCH", "GET"])
def handler():
    payload = request.get_json()
    metodo = request.method
    doc_id = payload.get("id")
    doc_data = payload.get("data", {})

    # 1. GET – Verificación y auditoría previa
    if metodo == "GET":
        existing = get_existing_document(doc_id)
        if existing:
            return jsonify({"status": "existe", "data": existing}), 200
        return jsonify({"status": "no encontrado", "data": {}}), 404

    # 2. Validación de duplicados y campos críticos
    if metodo in ["POST", "PATCH"]:
        if is_duplicate(doc_data):
            return jsonify({"error": "duplicado detectado"}), 409

        if not validate_essential_fields(doc_data):
            if not payload.get("flag_validar_automaticamente"):
                return jsonify({"error": "Faltan campos críticos: rol, contexto, instrucciones"}), 400

    # 3. POST – Crear nuevo documento (si no existe)
    if metodo == "POST":
        if doc_id in notion_data:
            return jsonify({"error": "ya existe"}), 409

        doc_data["origen"] = doc_data.get("origen", "creado_por_handler")
        doc_data["version"] = doc_data.get("version", "v1")
        doc_data["estado"] = "activo"
        doc_data["historial_acciones"] = []
        notion_data[doc_id] = doc_data

        log_action(doc_id, "CREACION")
        return jsonify({"status": "creado", "data": notion_data[doc_id]}), 201

    # 4. PATCH – Actualizar documento (si mejora)
    if metodo == "PATCH":
        if doc_id not in notion_data:
            return jsonify({"error": "documento no encontrado"}), 404

        if check_if_manual_entry(notion_data[doc_id]):
            return jsonify({"error": "documento sagrado (creado manualmente), no modificable"}), 403

        for k, v in doc_data.items():
            if v and k != "id":
                notion_data[doc_id][k] = v

        log_action(doc_id, "ACTUALIZACION")
        return jsonify({"status": "actualizado", "data": notion_data[doc_id]}), 200

    return jsonify({"error": "metodo no permitido"}), 405

# --- LIMPIEZA DE DUPLICADOS ---
@app.route("/limpiar_duplicados", methods=["POST"])
def eliminar_duplicados():
    vistos = set()
    eliminados = []
    for doc_id, doc in list(notion_data.items()):
        key = (doc.get("nombre"), doc.get("origen"))
        if key in vistos:
            eliminados.append(doc_id)
            del notion_data[doc_id]
        else:
            vistos.add(key)
    return jsonify({"eliminados": eliminados}), 200

# --- EJECUCIÓN ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)
