from flask import Flask, request, jsonify

app = Flask(__name__)

# =====================
# 📘 Módulo de Activación Central de Agentes ProMax
# =====================

AGENTES = {
    "nivel_1_nucleo_estrategico_y_directivo": [
        "Agente C0 – CEO",
        "Agente C1 – Cerebro Creativo / Generativo",
        "Agente C2 – Cerebro Técnico / Estratégico",
        "Infra Builder IA",
        "Prompt Engineering Pro Max",
        "Agente de Guiones y Storytelling Creativo Pro Max",
        "Agente Video Pipeline Master"
    ],
    "nivel_2_operativo_tecnico_y_productivo": [
        "Agente Cloud Creator Pro Max",
        "Agente de Creación y Optimización de Vídeos de alto nivel",
        "Agente de Diseño Gráfico y Desarrollo Digital de alto nivel",
        "Agente de Escritura de alto nivel",
        "Agente de Ilustraciones e Imágenes de alto nivel",
        "Agente Especialista de Adobe Suite de alto nivel",
        "Agente Especialista de ETSY de alto nivel",
        "Agente Experto Exclusivo de Canva",
        "Agente Shopify + Printify/Printful",
        "Agente SEO de alto nivel",
        "Agente: music_sound_engineer",
        "Agente: perplexity_research_master"
    ],
    "nivel_3_comunicacion_legalidad_y_expansion": [
        "Agente de Publicaciones en Redes Sociales Pro Max Vivo",
        "Agente de Marketing y ADS Pro Max",
        "Agente de Originalidad & Protección Creativa Pro Max",
        "Agente de Protección Legal & Propiedad Intelectual Pro Max",
        "Agente de Publicación y Moderación de Contenidos de Alto Nivel",
        "Agente de Reportes & Analytics Pro Max",
        "Agente Gemini Pro Max",
        "Agente Cross Promotion Coordinator"
    ]
}

@app.route('/activar_agentes', methods=['POST'])
def activar_agentes():
    data = request.json
    accion = data.get("accion", "desplegar")
    contexto = data.get("contexto", "infraestructura")

    response = {
        "status": "activado",
        "accion": accion,
        "contexto": contexto,
        "niveles": {},
        "mensaje": "Todos los agentes han sido activados según lógica contextual del ecosistema ProMax."
    }

    for nivel, lista in AGENTES.items():
        response["niveles"][nivel] = {
            "total_agentes": len(lista),
            "agentes": lista,
            "estado": "activo",
            "comentario": f"{nivel.replace('_', ' ').capitalize()} desplegado correctamente."
        }

    return jsonify(response), 200

# =====================
# 🔁 Ejecución del servidor (para entorno local o testing)
# =====================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
