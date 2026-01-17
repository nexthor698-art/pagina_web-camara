from flask import Flask, request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

# Lista temporal para guardar las fotos hasta que tu PC las pida
cola_fotos = []

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json.get('image')
    if data:
        cola_fotos.append(data) # Guarda la imagen en memoria
        return jsonify({"status": "recibida"}), 200
    return "Error", 400

@app.route('/get_photos', methods=['GET'])
def get_photos():
    global cola_fotos
    # Enviamos todas las fotos acumuladas y vaciamos la lista
    fotos_a_enviar = list(cola_fotos)
    cola_fotos = []
    return jsonify({"photos": fotos_a_enviar})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
