# 🧠 Handler de Columnas para Notion – Infraestructura IA Core

Este script en Python automatiza la gestión de columnas en una base de datos de Notion. Está diseñado para integrarse como un servicio web vía Flask y es parte fundamental de la infraestructura técnica del agente `InfraBuilder IA`.

---

## ⚙️ ¿Qué hace este script?

- Conecta con la API de Notion.
- Consulta las columnas actuales de una base de datos.
- Crea automáticamente las columnas faltantes con formato `multi_select`.
- Expone un endpoint para ejecutar esta acción de forma programada o externa.

---

## 🌍 Endpoint disponible

- **Ruta:** `/crear_columnas`
- **Método:** `POST`
- **Respuesta:** JSON con columnas creadas y columnas que ya existían.
- **Puerto de ejecución por defecto:** `5000` (`Flask`)

---

## 📦 Dependencias requeridas

- `Flask`
- `requests`
- Python ≥ 3.8

### Instalación:

```bash
pip install flask requests
```

---

## 🔐 Variables de entorno necesarias

| Variable             | Descripción                                   |
|----------------------|-----------------------------------------------|
| `NOTION_TOKEN`       | Token de acceso a la API de Notion            |
| `NOTION_DATABASE_ID` | ID de la base de datos en Notion              |

### Ejemplo:

```bash
export NOTION_TOKEN="secret_abc123..."
export NOTION_DATABASE_ID="abcd1234efgh..."
```

---

## 🧱 Estructura JSON gestionada

```json
{
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
```

---

## 🚀 Ejecución local (modo desarrollo)

```bash
python PY-HANDLER-NOTION-COLUMNS-V1.py
```

El servidor Flask iniciará y quedará a la espera de peticiones `POST` en:

```
http://localhost:5000/crear_columnas
```

---

## 🛡 Seguridad y mantenimiento

- No guarda tokens en disco.
- Se recomienda ejecutarlo dentro de un entorno virtual.
- Validado en `MacOS` y `Linux`.

---

## ✍️ Autor

**Infra Builder IA**  
Supervisor técnico de infraestructura  
Proyecto: BestanleyCreations  
Integración: Notion API | Flask | Python
