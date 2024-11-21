from datetime import datetime
import time


def rule(packet, tcp_packets, db):
    """Règle TCPConnect Flood:
    Un flood TCP connect va effectuer une connexion TCP en très grand nombre
    Si le port est ouvert le serveur acceptera la connexion SYN -> SYN ACK -> ACK -> Reset ACK
    Sinon le port est fermé et le serveur refusera la connexion SYN -> Reset ACK
    """

    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0):
        rule.time_window = db.get_key("tcpconnectflood_time", 60)
        rule.seuil = db.get_key("tcpconnectflood_count", 100)

    # Comptage du nombre de scan tcp connect acceptés et refusés
    tcpconnectdeny_count = tcp_packets.count_packet_of_type(["S", "RA"], rule.time_window, True)
    tcpconnectaccept_count = tcp_packets.count_packet_of_type(["S", "SA", "A", "RA"], rule.time_window, True)

    if (tcpconnectaccept_count + tcpconnectdeny_count >= rule.seuil):
        db.send_alert(datetime.now(), 5, None, "TCPConnect Flood", packet['IP'].src, packet['IP'].dst, proto="TCP", reason="Détection de nombreux patterns de Syn->SynACK->ACK->Reset ACK et Syn->Reset ACK", act="Alerte") 
        print(f"Alerte, seuils dépassés, risque de TCPconnect Flood")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0

