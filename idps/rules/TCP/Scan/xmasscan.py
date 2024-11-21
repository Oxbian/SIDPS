from datetime import datetime
import time


def rule(packet, tcp_packets, db):
    """Règle XMAS Scan:
    Un XMAS Scan va envoyer des requêtes TCP avec le flag Fin, Push, Urg
    Si le port est ouvert alors le serveur répondra pas
    Sinon le port est fermé et le serveur répondra: Reset ACK
    """
    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0):
        rule.time_window = db.get_key("xmasscan_time", 180)
        rule.seuil = db.get_key("xmasscan_count", 5)

    # Comptage du nombre de scan XMAS acceptés et refusés
    xmasdeny_count = tcp_packets.count_packet_of_type(["FPU", "RA"], rule.time_window, True)
    xmasaccept_count = tcp_packets.count_packet_of_type(["FPU"], rule.time_window, True)

    if (xmasaccept_count + xmasdeny_count >= rule.seuil):
        db.send_alert(datetime.now(), 5, None, "XMAS scan", packet['IP'].src, packet['IP'].dst, proto="TCP", reason="Détection de nombreux patterns de Fin Push Urg -> rien et Fin Push Urg->Reset ACK", act="Alerte")
        print(f"Alerte, seuil dépassés, risque de XMAS Scan")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
