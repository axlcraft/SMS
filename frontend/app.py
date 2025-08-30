# /frontend/app.py

from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)

# Obtén la URL del API Gateway desde las variables de entorno.
# Esta variable debe estar configurada en el docker-compose.yml.
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

@app.route("/")
def index():
    """Ruta de la página de inicio."""
    
    # TODO: Haz una llamada al API Gateway para obtener datos, si es necesario.
    # Por ejemplo, para obtener la lista de items de un servicio:
    # try:
    #     response = requests.get(f"{API_GATEWAY_URL}/api/v1/[recurso]")
    #     response.raise_for_status()  # Lanza un error para códigos de estado 4xx/5xx
    #     items = response.json()
    # except requests.exceptions.RequestException as e:
    #     print(f"Error al conectar con el API Gateway: {e}")
    #     items = []

    # Pasa los datos a la plantilla para renderizarlos.
    return render_template("index.html", title="Inicio")

@app.route("/new-item", methods=["GET","POST"])
def new_item():
    """Ruta para crear un nuevo ítem."""
    if request.method == "POST":
        item_data = {
            "systolic_pressure": int(request.form.get("systolic_pressure")),
            "diastolic_pressure": int(request.form.get("diastolic_pressure")),
            "heart_rate": int(request.form.get("heart_rate")),
            "weight": float(request.form.get("weight"))
        }
        # TODO: Envía los datos al API Gateway para crear un nuevo recurso.
        try: 
            response = requests.post(f"{API_GATEWAY_URL}/api/v1/metrics/create-metrics", json=item_data)
            print(response.text)
            response.raise_for_status()
            return redirect(url_for("index"))
        except requests.exceptions.RequestException as e:
            print(f"Error al crear el ítem en: {e}")
            return "Error al crear el ítem.", 500
            
    return render_template("form.html", title="Nuevo Ítem")
    # elif request.method == "GET":
    #     # TODO: Haz una llamada al API Gateway para obtener datos, si es necesario.
    #     # Por ejemplo, para obtener la lista de items de un servicio:
    #     try:
    #         response = requests.get(f"{API_GATEWAY_URL}/api/v1/[recurso]")
    #         response.raise_for_status()  # Lanza un error para códigos de estado 4xx/5xx
    #         items = response.json()
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error al conectar con el API Gateway: {e}")
    #         items = []

    # Pasa los datos a la plantilla para renderizarlos.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            response = requests.post(f"{API_GATEWAY_URL}/auth/login", json={"email": email, "password": password})
            response.raise_for_status()
            # Puedes guardar la sesión en cookies si lo deseas
            return redirect(url_for("index"))
        except requests.exceptions.RequestException as e:
            print(f"Error al iniciar sesión: {e}")
            return "Error al iniciar sesión.", 500
    return render_template("sesion.html", title="Iniciar Sesión")

@app.route("/registro", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            response = requests.post(f"{API_GATEWAY_URL}/auth/register", json={"email": email, "password": password})
            response.raise_for_status()
            return redirect(url_for("login"))
        except requests.exceptions.RequestException as e:
            print(f"Error al registrar usuario: {e}")
            return "Error al registrar usuario.", 500
    return render_template("registro.html", title="Registrar")

@app.route("/medico")
def medico():
    return render_template("medico.html", title="Médico")

@app.route("/grafica", methods=["GET"])
def grafica():
    

    
    
    
    return render_template("grafica.html", title="Gráfica")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

