# Générateur d'alertes CEF (Common Event Format)
# Pratique pour le moteur de corrélation et le site web

# Une alerte CEF est formattée de cette façon:
# CEF:Version|Device Vendor|Device Product|Device Version|Device Event Class ID|Name|Severity|[Extension]

import mysql.connector
import time
import random
from datetime import datetime


def generate_alert(alert_type):
    # Dictionnaire pour différents types d'alertes réseau et fichiers
    alert_templates = {
        "network": {
            "Syn Flood": {
                "Device_event_class_id": "1001",
                "name": "Syn Flood Detected",
                "src": f"{generate_ip()}",
                "dst": f"{generate_ip()}",
                "agent_severity": "8"
            },
            "Port Scanning": {
                "Device_event_class_id": "1002",
                "name": "Port Scanning Activity",
                "src": f"{generate_ip()}",
                "dst": f"{generate_ip()}",
                "cs1": f"{generate_ports()}",
                "agent_severity": "5"
            }
        },
        "file": {
            "Suspicious File Creation": {
                "Device_event_class_id": "2001",
                "name": "Suspicious File Created",
                "fname": f"{generate_filename()}",
                "fsize": f"{random.randint(10, 1000)}kb",
                "agent_severity": "7"
            },
            "Critical File Deletion Attempt": {
                "Device_event_class_id": "2002",
                "name": "Critical File Deletion Attempt",
                "fname": f"{generate_filename()}",
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

def generate_alerts(conn, cursor, main_headers):
    # Récupérer ces données depuis une fonction
    alertes = ["Syn Flood", "Port Scanning", "Suspicious File Creation", "Critical File Deletion Attempt"]

    while True:
        data = generate_alert(random.choice(alertes))
        merged = main_headers.copy()
        merged.update(data)

        # Préparer la requête SQL d'insertion
        sql_query = """
        INSERT INTO alertes (
            cef_version, date_alerte, event_gravite, device_product,
            device_vendor, device_version, alerte_name, sourceAddress,
            destinationAddress, destinationPort, sourcePort, protocol,
            applicationProtocol, reason, action, commentaire
        ) VALUES (
            %(cef_version)s, %(date_alerte)s, %(event_gravite)s, %(device_product)s,
            %(device_vendor)s, %(device_version)s, %(alerte_name)s, %(src)s,
            %(dst)s, %(destinationPort)s, %(sourcePort)s, %(protocol)s,
            %(applicationProtocol)s, %(reason)s, %(action)s, %(commentaire)s
        );
        """

        # Paramètres pour la requête SQL
        params = {
            "cef_version": merged["CEF"],
            "date_alerte": datetime.now(),
            "event_gravite": int(merged["agent_severity"]),
            "device_product": merged["Device Product"],
            "device_vendor": merged["Device Vendor"],
            "device_version": merged["Device Version"],
            "alerte_name": merged["name"],
            "src": merged["src"],
            "dst": merged["dst"],
            "destinationPort": None,  # A définir si disponible
            "sourcePort": None,  # A définir si disponible
            "protocol": "TCP",  # Par défaut, à adapter si besoin
            "applicationProtocol": "N/A",  # À ajuster en fonction des besoins
            "reason": "Suspicious activity detected",  # Exemple, à adapter
            "action": "Alerted",  # Exemple d'action
            "commentaire": ""  # Optionnel
        }

        # Exécution de la requête d'insertion
        cursor.execute(sql_query, params)
        conn.commit()

        # Attente avant de générer la prochaine alerte
        time.sleep(random.randint(1, 10))

def main():
    # Connexion à la base de données MySQL/MariaDB
    conn = mysql.connector.connect(
        host="172.20.2.10",  # À adapter selon votre configuration
        database="sidps",  # Nom de la base de données
        user="sidps",  # Nom d'utilisateur
        password="SUPERPASSWORD",  # Mot de passe
        port=3306  # Port MySQL par défaut (peut être 3306 ou autre selon la configuration)
    )

    cursor = conn.cursor()

    # En-têtes généraux
    CEF_version = 1
    Device_vendor = "ArKa"
    Device_product = "SIDPS"
    Device_version = "vAlpha"

    main_headers = {
        "CEF": CEF_version,
        "Device Vendor": Device_vendor,
        "Device Product": Device_product,
        "Device Version": Device_version
    }

    # Lancer la génération d'alertes
    generate_alerts(conn, cursor, main_headers)

    # Fermer la connexion à la base de données
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
