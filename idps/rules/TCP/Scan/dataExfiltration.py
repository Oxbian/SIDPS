from collections import defaultdict
from scapy.all import IP
import time

data_transfer = defaultdict(lambda: {"current": 0, "daily": 0, "last_reset": time.time()})

def rule(packet, _, db):
    """Règle pour détecter une exfiltration de données importantes."""
    global data_transfer

    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        payload_size = len(packet[IP].payload)

        # Mettre à jour le volume de données transférées
        current_time = time.time()
        if current_time - data_transfer[src_ip]["last_reset"] > rule.reset_time:
            data_transfer[src_ip]["daily"] = 0
            data_transfer[src_ip]["last_reset"] = current_time

        data_transfer[src_ip]["current"] += payload_size
        data_transfer[src_ip]["daily"] += payload_size

        # Déclencher une alerte si un seuil est atteint
        if data_transfer[src_ip]["current"] > rule.seuil_session:
            alert = {
                "type": "Exfiltration de données détectée (instantané)",
                "source_ip": src_ip,
                "destination_ip": dst_ip,
                "volume": data_transfer[src_ip]["current"] / (1024 ** 3),
                "threshold": rule.seuil_session / (1024 ** 3),
                "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            }
            db.save_alert(alert)
            data_transfer[src_ip]["current"] = 0  # Réinitialiser pour les prochaines sessions

        if data_transfer[src_ip]["daily"] > rule.seuil_journalier:
            alert = {
                "type": "Exfiltration de données détectée (journalière)",
                "source_ip": src_ip,
                "volume": data_transfer[src_ip]["daily"] / (1024 ** 3),
                "threshold": rule.seuil_journalier / (1024 ** 3),
                "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            }
            db.save_alert(alert)

rule.reset_time = 24 * 3600  # 24 heures en secondes
rule.seuil_session = 5 * 1024 * 1024 * 1024  # 5 Go en octets
rule.seuil_journalier = 50 * 1024 * 1024 * 1024  # 50 Go en octets