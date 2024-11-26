from datetime import datetime
import time


def rule(packet, objets):
    """Règle Fin Scan:
    Un Fin Scan va envoyer des requêtes TCP avec le flag Fin
    Si le port est ouvert alors le serveur répondra pas
    Sinon le port est fermé et le serveur répondra: Reset ACK
    """

    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0 and rule.ban_time == 0):
        rule.time_window = objets["config"].get("finscan_time", 180)
        rule.seuil = objets["config"].get("finscan_count", 5)
        rule.ban_time = objets["config"].get("finscan_bantime", 300)

    # Comptage du nombre de scan fin acceptés et refusés
    findeny_count = objets["tcp_packets"].count_packet_of_type(["F", "RA"], rule.time_window, True)
    finaccept_count = objets["tcp_packets"].count_packet_of_type(["F"], rule.time_window, True)

    if (findeny_count + finaccept_count >= rule.seuil):
        objets["database"].send_alert(datetime.now(), 5, None, "Fin scan", objets["pkt_origin"][0], objets["pkt_origin"][2], proto="TCP", reason="Détection de nombreux patterns de Fin->Reset Ack et Fin->rien", act="Alerte")
        objets["iptables_manager"].add_rule("iptables -I FORWARD -s " + objets["pkt_origin"][0] + " -j DROP", rule.ban_time)
        print("Alerte, seuil dépassés, risque de Fin Scan")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
rule.ban_time = 0
