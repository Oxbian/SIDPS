from datetime import datetime
import time


def rule(packet, objets):
    """Règle Null Scan:
    Un Null Scan va envoyer des requêtes TCP avec aucun flag d'actif
    Si le port est ouvert alors le serveur ne répondra pas
    Sinon le port est fermé et le serveur répondra: Reset ACK
    """
    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0 and rule.ban_time == 0):
        rule.time_window = objets["config"].get("nullscan_time", 180)
        rule.seuil = objets["config"].get("nullscan_count", 5)
        rule.ban_time = objets["config"].get("nullscan_bantime", 300)

    # Comptage du nombre de scan null acceptés et refusés
    nulldeny_count = objets["tcp_packets"].count_packet_of_type(["", "RA"], rule.time_window, True)
    nullaccept_count = objets["tcp_packets"].count_packet_of_type([""], rule.time_window, True)

    if (nullaccept_count + nulldeny_count >= rule.seuil):
        objets["database"].send_alert(datetime.now(), 5, None, "Null scan", objets["pkt_origin"][0], objets["pkt_origin"][2], proto="TCP", reason="Détection de nombreux patterns de None->Reset Ack et None -> rien", act="Alerte")
        objets["iptables_manager"].add_rule("iptables -I FORWARD -s " + objets["pkt_origin"][0] + " -j DROP", rule.ban_time)
        print("Alerte, seuil dépassés, risque de Null Scan")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
rule.ban_time = 0
