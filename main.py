from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app)  # Esto es vital para que Netlify pueda enviar datos

cola_fotos = []

# Si entras a la URL normal, esto evita el error 404
@app.route('/')
def home():
    return "Servidor Funcionando", 200

# Esta es la ruta donde la web ENVÍA las fotos
@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json.get('image')
        if data:
            cola_fotos.append(data)
            return jsonify({"status": "ok"}), 200
        return "No data", 400
    except:
        return "Error", 500

# Esta es la ruta donde tu PC DESCARGA las fotos
@app.route('/get_photos', methods=['GET'])
def get_photos():
    global cola_fotos
    enviar = list(cola_fotos)
    cola_fotos.clear()
    return jsonify({"photos": enviar})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
