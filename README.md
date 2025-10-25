## q hace:
- captura teclas q se presionan mientras se ejecuta.
- envia logs en tiempo real al server flask en localhost, osea a mi compu de informatica seria
- guarda cada sesion en un archivo local enumerado con el fin de no sobreescribirlo y almacenarlo en caso de un reinicio o algo x el estilo
- el server tambien guarda cada post en archivos enumerados como 'recived1.txt', 'recived2.txt', etc... con timestamp y direccion ip de origen

---
## requisitos:
- Python 3.13+
- pip, te recomiendo usar un entorno virtual
- librerias de py:
 - 'pynput'
 - 'requests'
 - 'Flask'
---

## ns q os usas pero linux/windows: 
- abri powershell o la shell q tengas y pone:
 - python -m venv venv

- activa el entorno:
 - linux:
    - source venv/bin/activate
 - windows:
    - venv\Scripts\activate

- instala las dependencias:
    - pip install Flask requests pynput


---

## para usarlo:
# correr el server:
- entra al proyecto q te clonaste de github con:
 - cd server
- y ejecutalo con:
 - python server.py
y se crea automaticamente la carpeta received_logs donde se guardan todos los logs q recive, el server queda escichando en localhost:8080/log pq mi server va a estar en red local.

# correr el keylogger:
- cd keylogger
- pip install Flask requests pynput pyinstaller
- python keylogger.py

_las pulsaciones se envian en tiempo real al server.
_se guarda un archivo temporal llamado temp_log.txt mientras se ejecuta
_ para terminar y guardar la sesion final: presiona ESC
_se crea un archivo logN.txt con toda la sesion, no se sobreescribe arvchivos anteriores.

pd: en BATCH_SIZE ubicado en keylogger.py podes cambiar el numero de teclas a enviar en el log, osea cambias el valor de 1 a 10 por ejemplo y cada 10 teclas q toque le van a llegar al server. te lo deje comentado para q lo entiendas mejor.

che hay q ponernos un nombre de grupo hacker como en las peliculas viste estaria copado.