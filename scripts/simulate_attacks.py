import urllib.request
import urllib.error
import json
import time
import random
from datetime import datetime

API_URL = "http://localhost:8000/api/v1/alerts"

SEVERITIES = ["INFO", "WARNING", "CRITICAL"]
ALERT_TYPES = ["WAF_SQL_INJECTION", "DDoS_ATTEMPT", "UNAUTHORIZED_ACCESS", "MALWARE_SIGNATURE", "PORT_SCAN", "DATA_EXFILTRATION"]
IPS = ["192.168.1.10", "10.0.0.45", "172.16.0.8", "203.0.113.5", "198.51.100.22", "45.33.18.12", "185.15.2.3"]

print("=====================================================")
print("🛡️  Aegis Zero-Trust: Simulador de Tráfico Malicioso 🛡️")
print("=====================================================")
print(f"Enviando alertas a: {API_URL}")
print("Presiona Ctrl+C para detener la simulación.\n")

try:
    while True:
        data = {
            "source_ip": random.choice(IPS),
            "severity": random.choice(SEVERITIES),
            "alert_type": random.choice(ALERT_TYPES),
            "description": f"Simulated attack payload detected on edge proxy at {datetime.now().strftime('%H:%M:%S')}"
        }
        
        req = urllib.request.Request(
            API_URL, 
            data=json.dumps(data).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}, 
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                print(f"[+] ALERTA PUSHED -> IP: {data['source_ip']} | Tipo: {data['alert_type']} | Nivel: {data['severity']}")
        except urllib.error.URLError as e:
            print(f"[-] Falló la conexión: {e.reason}. ¿Está Uvicorn encendido en el puerto 8000?")
            
        # Espera aleatoria entre 1.5 y 4 segundos para simular oleadas irregulares
        time.sleep(random.uniform(1.5, 4.0))
        
except KeyboardInterrupt:
    print("\n\nSimulación detenida por el operador. ¡Buen trabajo protegiendo el perímetro!")
