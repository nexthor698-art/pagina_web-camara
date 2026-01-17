from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app)

# Lista para guardar las fotos temporalmente
cola_fotos = []

@app.route('/')
def home():
    # Esto confirma que el servidor funciona
    return jsonify({"status": "servidor_activo", "info": "usa /get_photos para descargar"}), 200

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json.get('image')
        if data:
            cola_fotos.append(data)
            return jsonify({"status": "recibida"}), 200
        return jsonify({"error": "sin datos"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_photos', methods=['GET'])
def get_photos():
    global cola_fotos
    # Enviamos lo que hay y limpiamos
    copia = list(cola_fotos)
    cola_fotos.clear()
    # FORZAMOS que la respuesta sea JSON puro
    return jsonify({"photos": copia})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
