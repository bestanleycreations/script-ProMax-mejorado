import pickle
import os
import io
import yaml
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime

# SCOPES para Google Drive (lectura únicamente por seguridad)
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN_PICKLE_FILE = 'token_google_drive.pickle'
CREDENTIALS_JSON_FILE = 'credentials.json'

def authenticate_google_drive():
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_JSON_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def list_files(service, mime_type_filter=None):
    results = service.files().list(
        q=f"mimeType != 'application/vnd.google-apps.folder'" + (f" and mimeType='{mime_type_filter}'" if mime_type_filter else ""),
        pageSize=10,
        fields="files(id, name, mimeType, modifiedTime)").execute()
    return results.get('files', [])

def download_and_parse_file(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    ext = file_name.split('.')[-1]
    try:
        if ext in ['yml', 'yaml']:
            return yaml.safe_load(fh)
        elif ext == 'json':
            return json.load(fh)
        elif ext in ['py', 'js']:
            return fh.read().decode('utf-8')
        else:
            return fh.read().decode('utf-8')
    except Exception as e:
        return f"Error al procesar {file_name}: {e}"

if __name__ == '__main__':
    print("🔐 Autenticando con Google Drive...")
    service = authenticate_google_drive()
    if not service:
        print("❌ Error al autenticar. Verifica tu archivo credentials.json.")
        exit()

    print("📁 Listando archivos relevantes...")
    files = list_files(service)
    if not files:
        print("❌ No se encontraron archivos.")
    else:
        for file in files:
            print(f"\n🧾 Nombre: {file['name']}")
            print(f"🗂️ Tipo MIME: {file['mimeType']}")
            print(f"🕒 Modificado: {file['modifiedTime']}")
            print("📥 Descargando y procesando contenido...")
            content = download_and_parse_file(service, file['id'], file['name'])
            print("🧠 Resultado:")
            print(content)
