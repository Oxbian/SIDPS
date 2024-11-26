from datetime import datetime, time, timedelta
from scapy.all import IP

# Dictionnaire pour stocker les dernières alertes envoyées pour chaque IP
last_alert_time = {}

def rule(packet, _, db):
    """
    Règle pour détecter l'activité réseau entre une plage horaire donnée.
    """
    global last_alert_time

    if IP in packet:

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        # Obtenir l'heure actuelle
        current_time = datetime.now()

        # Vérifier si l'heure est dans la plage
        if rule.start_time <= current_time.time() or current_time.time() <= rule.end_time:
            # Vérifier si une alerte a déjà été envoyée récemment pour cette IP
            if src_ip in last_alert_time:
                time_since_last_alert = current_time - last_alert_time[src_ip]
                if time_since_last_alert < timedelta(minutes=5):  # 5 minutes de délai
                    return  # Ne pas envoyer une nouvelle alerte

            # Envoyer une alerte
            db.send_alert(
                current_time, 
                5,
                None, 
                f"Activité réseau détectée entre {rule.start_time} et {rule.end_time}", 
                src_ip,
                dst_ip, 
                proto="TCP",
                reason=f"Activité réseau à {current_time.time()}", 
                act="Alerte"
            )
            print(f"Alerte : activité réseau détectée à {current_time.time()} entre {src_ip} et {dst_ip}")

            # Mettre à jour le temps de la dernière alerte pour cette IP
            last_alert_time[src_ip] = current_time

# Définir la plage horaire
rule.start_time = time(21, 0)
rule.end_time = time(6, 0)
