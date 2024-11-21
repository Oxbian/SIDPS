from collections import defaultdict
from scapy.all import IP
import time
from datetime import datetime

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

        print(data_transfer[src_ip]["current"])

        # Exfiltration de données instantané
        if data_transfer[src_ip]["current"] > rule.seuil_session:
            db.send_alert(
                datetime.now(), 
                5, 
                None, 
                "Exfiltration de données détectée (instantané)", 
                src_ip,
                dst_ip, 
                proto = "TCP",
                reason="Exfiltration de données détectée (instantané)", 
                act="Alerte"
                )
            data_transfer[src_ip]["current"] = 0  # Réinitialiser pour les prochaines sessions
            print(f"Alerte, data transfer, transfert instantané important")

        # Exfiltration de données journalière
        if data_transfer[src_ip]["daily"] > rule.seuil_journalier:
            db.send_alert(
                datetime.now(), 
                5, 
                None, 
                "Exfiltration de données détectée (journalière)", 
                src_ip,
                dst_ip, 
                proto = "TCP",
                reason="Exfiltration de données détectée (journalière)", 
                act="Alerte"
                )
            print(f"Alerte, data transfer, transfert journalier important")


rule.reset_time = 24 * 3600  # 24 heures en secondes
rule.seuil_session = 5 * 1024 * 1024 * 1024  # 5 Go en octets
rule.seuil_journalier = 50 * 1024 * 1024 * 1024  # 50 Go en octets