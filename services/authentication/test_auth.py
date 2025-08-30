import requests

def test_auth_health():
    r = requests.get("http://localhost:8001/health")
    print("Auth health:", r.status_code, r.text)

def test_metrics_health():
    r = requests.get("http://localhost:8002/health")
    print("Metrics health:", r.status_code, r.text)

def test_register_and_login():
    BASE_URL_AUTH = "http://localhost:8001/auth"
    # Registro
    payload = {"email": "testuser@example.com", "password": "testpass123"}
    r = requests.post(f"{BASE_URL_AUTH}/register", json=payload)
    print("Register:", r.status_code, r.text)
    # Login
    r = requests.post(f"{BASE_URL_AUTH}/login", json=payload)
    print("Login:", r.status_code, r.text)
    if r.status_code == 200:
        session = r.json()
        print("Session:", session)
        # Obtener sesiones
        user_id = 1  # Asume que el usuario creado tiene id=1
        r = requests.get(f"{BASE_URL_AUTH}/sessions/{user_id}")
        print("Sessions:", r.status_code, r.text)

def main():
    test_auth_health()
    test_metrics_health()
    test_register_and_login()

if __name__ == "__main__":
    main()
