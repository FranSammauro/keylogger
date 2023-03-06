from flask import Flask, request

app = Flask(__name__)

#Comprovamos que la conexion a sido exitosa
@app.route('/')
def index():
    return 'Hello, World!'

# Nos conctamos a la ruta y puesto ya definidos con Flask
@app.route('/log', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        data = request.get_data()
        with open('log.txt', 'w') as f:
            f.write(data.decode('utf-8'))
        return 'datos enviados'
    else:
        return 'Error'

# Nos conectamos al puesto definido por nosotros
if __name__ == '__main__':
    app.run(debug=True, port=8080)
