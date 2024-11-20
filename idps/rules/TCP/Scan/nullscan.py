from datetime import datetime
import time


def rule(packet, tcp_packets, db):
    """Règle Null Scan:
    Un Null Scan va envoyer des requêtes TCP avec aucun flag d'actif
    Si le port est ouvert alors le serveur ne répondra pas
    Sinon le port est fermé et le serveur répondra: Reset ACK
    """
    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0):
        rule.time_window = db.get_key("nullscan_time", 180)
        rule.seuil = db.get_key("nullscan_count", 5)

    if tcp_packets.count_packet_of_type([""], rule.time_window, True) + tcp_packets.count_packet_of_type(["", "RA"], rule.time_window, True) >= rule.seuil:
        db.send_alert(datetime.now(), 5, None, "Null scan", packet['IP'].src, packet['IP'].dst, proto="TCP", reason="Détection de nombreux patterns de None->Reset Ack et None -> rien", act="Alerte")
        print(f"Alerte, seuil dépassés, risque de Null Scan")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
