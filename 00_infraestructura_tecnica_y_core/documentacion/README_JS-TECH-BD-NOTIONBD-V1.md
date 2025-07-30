# README – Handler HTTP GET desde GitHub para Infraestructura YAML

## 📌 Descripción
Este script automatizado realiza una **solicitud HTTP GET** para obtener un archivo `.yaml` de configuración alojado en un repositorio de GitHub. El propósito es facilitar la integración remota de estructuras YAML desde fuentes centralizadas, como parte del sistema de infraestructura inteligente de **Bestanley Creations**.

## ⚙️ Módulo Make Utilizado
- `http:ActionSendData` – v3

## 🔗 Endpoint objetivo
```http
GET https://raw.githubusercontent.com/bestanleycreations/script-ProMax-mejorado/main/00_infraestructura_tecnica_y_core/00_1_agentes_yamls_y_jsons/agente-infrabuilder-ia/AY-INFRA-BC-2025‑V1/AY‑INFRA‑BC‑2025‑V1.yaml
```

## 🧩 Parámetros del módulo
- **Method**: `GET`
- **Gzip**: `true`
- **Parse response**: `true`
- **Follow redirects**: `true`
- **Handle errors**: `true`

## 🔐 Encabezados (Headers)
```json
[
  {
    "name": "Authorization",
    "value": "Bearer [TOKEN_PRIVADO]"
  }
]
```

> **Nota**: El token debe ser sustituido dinámicamente mediante variable segura o encriptación.

## 🔄 Funcionalidad
- Descarga remota de YAMLs
- Lectura directa desde raw GitHub
- No realiza escritura (POST/PATCH)
- Uso exclusivo para **lectura e integración remota**

## 📁 Ubicación actual del JSON relacionado
```
./00_infraestructura_tecnica_y_core/documentacion/JS‑TECH‑BD‑NOTIONBD‑V1.json
```

## 📌 Observaciones
- Este handler no modifica Notion.
- No incluye payload.
- Su único propósito es facilitar la descarga estructurada de YAML remotos para análisis o posterior integración.

## 🏷 Tags internos
`infraestructura`, `handler`, `get`, `yaml`, `GitHub`, `bestanley`, `notion-columns`, `automatización`