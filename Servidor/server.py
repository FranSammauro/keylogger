# server.py
# tenes q tener flask, pip install Flask

from flask import Flask, request, abort
import os
import time
import threading

app = Flask(__name__)

# Directorio donde se guardan los logs recibidos
LOG_DIR = "received_logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Si qres usar autenticacion por token simple ponelo aca
# Si lo dejás como None, no se comprueba
API_KEY = None  # ej: "token_asdf" o None para desactivar

# Lock para evitar condiciones de carrera al crear archivos enumerados
_counter_lock = threading.Lock()

def get_next_server_filename(prefix="received", ext=".txt"):
    """
    Devuelve el siguiente nombre disponible: received1.txt, received2.txt, ...
    Protegido por un lock para uso concurrente.
    """
    with _counter_lock:
        counter = 1
        while True:
            name = f"{prefix}{counter}{ext}"
            path = os.path.join(LOG_DIR, name)
            if not os.path.exists(path):
                return path
            counter += 1

@app.route('/')
def index():
    return 'Server up. Send POST to /log', 200

@app.route('/log', methods=['POST'])
def receive_data():
    # verifica si la api key está configurada
    if API_KEY is not None:
        provided = request.headers.get("X-API-KEY")
        if provided != API_KEY:
            # 401 Unauthorized
            abort(401, description="Invalid API key")

    # obtiene los datos del body raw
    raw = request.get_data()
    if not raw:
        return "No data received", 400

    try:
        text = raw.decode('utf-8', errors='replace')
    except Exception:
        text = str(raw)

    # construye el contenido a guardar con meta
    meta = [
        f"Received at: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"From: {request.remote_addr}",
        f"Content-Length: {request.content_length}",
        f"Content-Type: {request.content_type}",
        "-" * 40,
    ]
    content_to_write = "\n".join(meta) + "\n" + text + "\n"

    # consigue el nombre de archivo disponible y guardar
    try:
        filepath = get_next_server_filename(prefix="received", ext=".txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content_to_write)
    except Exception as e:
        # Si falla al escribir, devolvemos error 500
        return f"Failed to write file: {e}", 500

    return "datos enviados", 200

if __name__ == '__main__':
    # Para que la maquina sea accesible desde otras compus de la LAN:
    print(f"Starting server. Logs will be saved in: {os.path.abspath(LOG_DIR)}")
    if API_KEY:
        print("API_KEY is set — server will require X-API-KEY header.")
    app.run(host='0.0.0.0', port=8080, debug=False)
