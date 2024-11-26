from collections import defaultdict
from scapy.all import IP
import time
from datetime import datetime

data_transfer = defaultdict(lambda: {"current": 0, "daily": 0, "last_reset": time.time()})
reset_time = 24 * 3600  # 24 heures en secondes
seuil_session = 0.5 * 1024 * 1024 * 1024  # 500 Mo en octets
seuil_journalier = 50 * 1024 * 1024 * 1024  # 50 Go en octets


def rule(packet, objets):
    """
    Règle pour détecter une exfiltration de données importantes.
    Actuellement, ne fonctionne pas pour un débit supérieur à 4Mo
    """
    global data_transfer

    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        payload_size = len(packet[IP].payload)

        # Mettre à jour le volume de données transférées
        current_time = time.time()
        if current_time - data_transfer[src_ip]["last_reset"] > reset_time:
            data_transfer[src_ip]["daily"] = 0
            data_transfer[src_ip]["last_reset"] = current_time

        data_transfer[src_ip]["current"] += payload_size
        data_transfer[src_ip]["daily"] += payload_size

        # Exfiltration de données instantané
        if data_transfer[src_ip]["current"] > seuil_session:
            objets["database"].send_alert(datetime.now(), 5, None, "Exfiltration de données détectée (instantané)", src_ip, dst_ip, proto = "TCP", reason="Exfiltration de données détectée (instantané)", act="Alerte")
            data_transfer[src_ip]["current"] = 0  # Réinitialiser pour les prochaines sessions
            print("Alerte, data transfer, transfert instantané important")

        # Exfiltration de données journalière
        if data_transfer[src_ip]["daily"] > seuil_journalier:
            objets["database"].send_alert(datetime.now(), 5, None, "Exfiltration de données détectée (journalière)", src_ip, dst_ip, proto = "TCP", reason="Exfiltration de données détectée (journalière)", act="Alerte")
            print("Alerte, data transfer, transfert journalier important")
