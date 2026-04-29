from flask import Flask, jsonify

app = Flask(__name__)

# --- Funciones de lógica (las que vamos a probar) ---

def sumar(a, b):
    return a + b

def es_palindromo(texto):
    texto = texto.lower().replace(" ", "")
    return texto == texto[::-1]

def calcular_descuento(precio, porcentaje):
    if porcentaje < 0 or porcentaje > 100:
        raise ValueError("El porcentaje debe estar entre 0 y 100")
    return precio - (precio * porcentaje / 100)

# --- Rutas de la API ---

@app.route('/')
def inicio():
    return jsonify({
        "mensaje": "API CI/CD funcionando correctamente",
        "version": "1.0.0",
        "status": "ok"
    })

@app.route('/sumar/<int:a>/<int:b>')
def ruta_sumar(a, b):
    resultado = sumar(a, b)
    return jsonify({"operacion": "suma", "resultado": resultado})

@app.route('/palindromo/<texto>')
def ruta_palindromo(texto):
    resultado = es_palindromo(texto)
    return jsonify({"texto": texto, "es_palindromo": resultado})

@app.route('/salud')
def salud():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
