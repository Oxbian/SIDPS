from datetime import datetime
import time


def rule(packet, objets):
    """Règle TCPConnect Scan:
    Un scan TCP connect va effectuer une connexion TCP en entier sur chaque port scanné.
    Si le port est ouvert le serveur acceptera la connexion SYN -> SYN ACK -> ACK -> Reset ACK
    Sinon le port est fermé et le serveur refusera la connexion SYN -> Reset ACK
    """

    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0 and rule.ban_time == 0):
        rule.time_window = objets["config"].get("tcpconnectscan_time", 180)
        rule.seuil = objets["config"].get("tcpconnectscan_count", 5)
        rule.ban_time = objets["config"].get("tcpconnectscan_bantime", 300)

    # Comptage du nombre de scan tcp connect acceptés et refusés
    tcpconnectdeny_count = objets["tcp_packets"].count_packet_of_type(["S", "RA"], rule.time_window, True)
    tcpconnectaccept_count = objets["tcp_packets"].count_packet_of_type(["S", "SA", "A", "RA"], rule.time_window, True)

    if (tcpconnectaccept_count + tcpconnectdeny_count >= rule.seuil):
        objets["database"].send_alert(datetime.now(), 5, None, "TCPConnect Scan", objets["pkt_origin"][0], objets["pkt_origin"][2], proto="TCP", reason="Détection de nombreux patterns de Syn->SynACK->ACK->Reset ACK et Syn->Reset ACK", act="Alerte")
        objets["iptables_manager"].add_rule("iptables -I FORWARD -s " + objets["pkt_origin"][0] + " -j DROP", rule.ban_time)
        print("Alerte, seuils dépassés, risque de TCPConnectScan")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
rule.ban_time = 0
