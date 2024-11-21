from datetime import datetime
import time


def rule(packet, tcp_packets, db):
    """Règle SYN Scan:
    Un SYNScan va envoyer des requêtes TCP avec le flag SYN
    Si le port est ouvert alors le serveur répondra: Syn ACK, puis le client Reset la connexion
    Sinon le port est fermé et le serveur répondra: Reset ACK
    """
    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0):
        rule.time_window = db.get_key("synscan_time", 180)
        rule.seuil = db.get_key("synscan_count", 5)

    # Comptage du nombre de scan syn acceptés et refusés
    syndeny_count = tcp_packets.count_packet_of_type(["S", "RA"], rule.time_window, True)
    synaccept_count = tcp_packets.count_packet_of_type(["S", "SA", "R"], rule.time_window, True)

    if (synaccept_count + syndeny_count >= rule.seuil):
        db.send_alert(datetime.now(), 5, None, "Syn scan", packet['IP'].src, packet['IP'].dst, proto="TCP", reason="Détection de nombreux patterns de Syn->SynACK->Reset et Syn->Reset ACK", act="Alerte")
        print(f"Alerte, seuil dépassés, risque de SynScan")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
