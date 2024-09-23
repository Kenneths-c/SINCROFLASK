from flask import Flask, jsonify
from pathlib import Path
import asyncio
import threading
import time
from sharepoint_manager import SharePointManager

app = Flask(__name__)

folder = "Documentos"
storage = Path("C:\\Users\\KENNETH\\Documents\\Documentos")

manager = SharePointManager(folder, storage)

# Ejecuta la sincronización en un hilo separado
def run_sync_once():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(manager.transfer_files())
    loop.close()  

def start_sync_thread():
    sync_thread = threading.Thread(target=run_sync_once)
    sync_thread.daemon = True
    sync_thread.start()

@app.route('/')
def home():
    return jsonify({"status": "Sincronización en curso"})

if __name__ == '__main__':
    start_sync_thread() 
    app.run(debug=True, use_reloader=False)  # Desactiva el recargador automático de Flask
