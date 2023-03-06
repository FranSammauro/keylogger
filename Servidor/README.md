##  Instalacion de librerias 

> Creacion del archivo para las librerias

```
requirements.txt
```


> Codigo del Archivo

```
click==8.1.3
colorama==0.4.6
Flask==2.2.3
importlib-metadata==6.0.0
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.2
Werkzeug==2.2.3
zipp==3.15.0
```

> Instalacion de las Librerias

```python
pip install -r ".\requirements.txt"
```
---------------------------------
##  Copiar el codigo para el Servidor

> Creamos el archivo para el servidor
```
server.py
```

```
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/log', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        data = request.get_data()
        with open('log.txt', 'w') as f:
            f.write(data.decode('utf-8'))
        return 'Data received successfully!'
    else:
        return 'Invalid request method'

if __name__ == '__main__':
    app.run(debug=True, port=8080)

```


> Ejecutamos el vervidor
```
python server.py
```