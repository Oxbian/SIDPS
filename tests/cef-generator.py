# Générateur d'alertes CEF (Common Event Format)
# Pratique pour le moteur de corrélation et le site web

# Une alerte CEF est formattée de cette façon:
# CEF:Version|Device Vendor|Device Product|Device Version|Device Event Class ID|Name|Severity|[Extension]

import redis
import time
import random

def generate_alert(alert_type):
    # Dictionnaire pour différents types d'alertes réseau et fichiers
    alert_templates = {
        "network": {
            "Syn Flood": {
                "Device_event_class_id": "1001",
                "name": "Syn Flood Detected",
                "src" : f"{generate_ip()}",
                "dst" : f"{generate_ip()}",
                "agent_severity": "8"
            },
            "Port Scanning": {
                "Device_event_class_id": "1002",
                "name": "Port Scanning Activity",
                "src" : f"{generate_ip()}",
                "dst" : f"{generate_ip()}",
                "cs1" : f"{generate_ports()}",
                "agent_severity": "5"
            }
        },
        "file": {
            "Suspicious File Creation": {
                "Device_event_class_id": "2001",
                "name": "Suspicious File Created",
                "fname" : f"{generate_filename()}",
                "fsize" : f"{random.randint(10,1000)}kb",
                "agent_severity": "7"
            },
            "Critical File Deletion Attempt": {
                "Device_event_class_id": "2002",
                "name": "Critical File Deletion Attempt",
                "fname" : f"{generate_filename()}",
                "agent_severity": "9"
            }
        }
    }

    # Sélectionner le bon template en fonction du type d'alerte
    category = "network" if alert_type in alert_templates["network"] else "file"
    alert_info = alert_templates[category].get(alert_type, {})

    if not alert_info:
        raise ValueError(f"Unknown alert type: {alert_type}")

    return alert_info

def generate_ip():
    # Générer une adresse IP aléatoire
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def generate_ports():
    # Générer une liste de ports scannés
    return ",".join(str(random.randint(20, 1024)) for _ in range(5))

def generate_filename():
    # Générer un nom de fichier aléatoire
    filenames = ["config.txt", "database.db", "system32.dll", "passwd", "shadow", "sensitive_data.doc"]
    return random.choice(filenames)

def generate_alerts(db, main_headers):
    # Récupérer ces données depuis une fonction
    alertes = ["Syn Flood", "Port Scanning", "Suspicious File Creation", "Critical File Deletion Attempt"]

    while (1):
        data = generate_alert(random.choice(alertes))
        merged = main_headers.copy()
        merged.update(data)
       
        # Ajout dans redis
        response = db.xadd("logs:alertes", merged)
        time.sleep(random.randint(1, 10))
        

def main():
    
    # Connexion à Redis (si besoin changer l'host et le port)
    db = redis.Redis(host='localhost', port=6379, decode_responses=True)

    # Pour une db en production (https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/)
    #db = redis.Redis(host="my-redis.cloud.redislabs.com", port=6379, username="default", password="secret", ssl=True, ssl_certfile="./redis_user.crt", ssl_keyfile="./redis_user_private.key", ssl_ca_certs="./redis_ca.pem")

    CEF_version=1
    Device_vendor="ArKa"
    Device_product="SIDPS"
    Device_version="vAlpha"

    main_headers = {"CEF": CEF_version, "Device Vendor" : Device_vendor, "Device Product" : Device_product, "Device_version" : Device_version}

    generate_alerts(db, main_headers)

if __name__ == "__main__":
    main()
