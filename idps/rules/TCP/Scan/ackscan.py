from datetime import datetime
import time


def rule(packet, tcp_packets, db):
    """Règle ACK Scan:
    Un ACK Scan va envoyer des requêtes TCP avec le flag ACK
    Si le firewall ne bloque pas, alors il répond avec le flag Reset
    Sinon il répond rien
    """
    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0):
        rule.time_window = db.get_key("ackscan_time", 180)
        rule.seuil = db.get_key("ackscan_count", 5)

    # Comptage nombre de scan ack acceptés et refusés
    ackdeny_count = tcp_packets.count_packet_of_type(["A", "R"], rule.time_window, True)
    ackaccept_count = tcp_packets.count_packet_of_type(["A"], rule.time_window, True)

    if (ackaccept_count + ackdeny_count >= rule.seuil):
        db.send_alert(datetime.now(), 5, None, "ACK scan", packet['IP'].src, packet['IP'].dst, proto="TCP", reason="Détection de nombreux patterns de Ack->Reset et Ack pas de réponse", act="Alerte")
        print(f"Alerte, seuil dépassés, risque d'Ack scan")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
