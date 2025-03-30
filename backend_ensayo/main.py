from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Imprimir la API_KEY cargada para verificar
print("API Key cargada:", os.getenv("API_KEY"))

# Configurar la API Key de Gemini (asegurarte de que esté bien configurada)
genai.configure(api_key=os.getenv("API_KEY"))

@app.route("/generar-ensayo", methods=["POST"])
def generar_ensayo():
    datos = request.json
    tema = datos.get("tema", "")

    # Validar que el tema esté presente en la solicitud
    if not tema:
        return jsonify({"error": "Debes proporcionar un tema"}), 400

    try:
        # Usar el modelo de Gemini para generar el ensayo
        modelo = genai.GenerativeModel("gemini-1.5-pro")  # Usamos el modelo Gemini correcto
        # Aquí se solicita un ensayo más largo y detallado con más párrafos
        prompt = (f"Escribe un ensayo detallado y largo sobre {tema}. "
                "El ensayo debe comenzar directamente con la introducción del tema, "
                "y no debe incluir frases como 'Aquí está el ensayo sobre...'. "
                "Debe contener al menos cuatro párrafos de desarrollo con argumentos y ejemplos, "
                "y una conclusión que resuma los puntos tratados. "
                "El ensayo debe tener una longitud de aproximadamente 1000 a 1500 palabras.")

        
        respuesta = modelo.generate_content(prompt)

        # Verificamos si la respuesta fue exitosa
        if respuesta:
            return jsonify({"ensayo": respuesta.text})
        else:
            return jsonify({"error": "No se pudo generar el ensayo"}), 500

    except Exception as e:
        # Capturamos errores y los devolvemos como respuesta
        return jsonify({"error": str(e)}), 500


# Iniciar el servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
