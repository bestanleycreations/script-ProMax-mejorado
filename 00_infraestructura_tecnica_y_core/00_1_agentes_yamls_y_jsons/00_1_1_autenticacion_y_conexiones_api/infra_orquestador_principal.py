from 00_infraestructura_tecnica_y_core.00_1_agentes_yamls_y_jsons.00_1_1_autenticacion_y_conexiones_api.authenticate_oauth import (
    authenticate_google_drive, list_files, download_and_parse_file
)

# --- Configuración inicial de InfraBuilder IA ---
# Opcional: Preparado para incorporar logging avanzado
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# Si tienes un ID de carpeta para configuraciones específicas, define aquí:
# RUTA_CONFIGS = "ID_DE_TU_CARPETA_DE_CONFIGURACIONES_EN_DRIVE"

def inicializar_sistema():
    print("InfraBuilder IA: 🚀 Iniciando el sistema 'Promax'...")

    global drive_service_global
    drive_service_global = authenticate_google_drive()

    if not drive_service_global:
        print("InfraBuilder IA: ❌ ¡Error crítico! No se pudo autenticar Google Drive. El sistema no puede proceder.")
        return False

    print("InfraBuilder IA: ✅ Google Drive autenticado con éxito.")
    return True

def gestionar_configuraciones_agentes():
    print("InfraBuilder IA: ⚙️ Gestionando configuraciones de agentes desde Google Drive...")

    if not drive_service_global:
        print("InfraBuilder IA: ⚠️ Servicio de Drive no disponible. Reintentando autenticación...")
        if not inicializar_sistema():
            return

    # files = drive_service_global.files().list(q=f"'{RUTA_CONFIGS}' in parents", ... )  # Activar si defines una ruta específica
    files_to_process = list_files(drive_service_global, mime_type_filter=None)

    if not files_to_process:
        print("InfraBuilder IA: 🔍 No se encontraron archivos de configuración en Google Drive.")
        return

    for file_item in files_to_process:
        file_name = file_item['name']
        file_id = file_item['id']

        if file_name.endswith(('.yml', '.yaml', '.json')):
            print(f"InfraBuilder IA: ⬇️ Descargando y procesando configuración: {file_name}")
            config_data = download_and_parse_file(drive_service_global, file_id, file_name)

            if isinstance(config_data, str) and config_data.startswith("Error"):
                print(f"InfraBuilder IA: ❌ Error al procesar {file_name}: {config_data}")
            else:
                print(f"InfraBuilder IA: ✨ Configuración de '{file_name}' cargada. Tipo: {type(config_data)}")
                # Aquí se pasa config_data al agente correspondiente si se desea
                # if 'agente_nombre' in config_data:
                #     print(f"InfraBuilder IA: Configuración para el agente {config_data['agente_nombre']}")
                # else:
                #     print("InfraBuilder IA: Configuración genérica cargada.")
        # else:
        #     print(f"InfraBuilder IA: ➡️ Archivo ignorado: {file_name}")

# --- Ejecución principal ---
if __name__ == '__main__':
    if inicializar_sistema():
        print("\nInfraBuilder IA: Sistema inicializado. Ejecutando tareas de gestión...")
        gestionar_configuraciones_agentes()
        print("\nInfraBuilder IA: Tareas completadas. Sistema listo para los 27 agentes.")
    else:
        print("InfraBuilder IA: ❌ No se pudo inicializar el sistema por errores críticos.")
