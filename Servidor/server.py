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
