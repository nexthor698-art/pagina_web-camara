from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os
import time

app = Flask(__name__)
# Esto permite que Netlify se comunique con Render
CORS(app)

# Carpeta donde se guardarán las fotos
UPLOAD_FOLDER = 'capturas'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return "Servidor de Procesamiento Activo", 200

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json.get('image')
        if not data:
            return "No image data", 400

        # Decodificar Base64
        header, encoded = data.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        # Nombre de archivo único basado en tiempo
        filename = f"foto_{int(time.time())}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        print(f"Imagen guardada: {filename}")
        return jsonify({"status": "success", "file": filename}), 200
    except Exception as e:
        print(f"Error: {e}")
        return str(e), 500

if __name__ == '__main__':
    # Render usa el puerto que le asigne el sistema
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
