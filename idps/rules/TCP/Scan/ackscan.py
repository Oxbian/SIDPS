from datetime import datetime
import time


def rule(packet, objets):
    """Règle ACK Scan:
    Un ACK Scan va envoyer des requêtes TCP avec le flag ACK
    Si le firewall ne bloque pas, alors il répond avec le flag Reset
    Sinon il répond rien
    """
    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0 and rule.ban_time == 0):
        rule.time_window = objets["config"].get("ackscan_time", 180)
        rule.seuil = objets["config"].get("ackscan_count", 5)
        rule.ban_time = objets["config"].get("ackscan_bantime", 300)

    # Comptage nombre de scan ack acceptés et refusés
    ackdeny_count = objets["tcp_packets"].count_packet_of_type(["A", "R"], rule.time_window, True)
    ackaccept_count = objets["tcp_packets"].count_packet_of_type(["A"], rule.time_window, True)

    if (ackaccept_count + ackdeny_count >= rule.seuil):
        objets["database"].send_alert(datetime.now(), 5, None, "ACK scan", objets["pkt_origin"][0], objets["pkt_origin"][2], proto="TCP", reason="Détection de nombreux patterns de Ack->Reset et Ack pas de réponse", act="Alerte")
        print("Alerte, seuil dépassés, risque d'Ack scan")
        objets["iptables_manager"].add_rule("iptables -I FORWARD -s " + objets["pkt_origin"][0] + " -j DROP", rule.ban_time)
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
rule.ban_time = 0
