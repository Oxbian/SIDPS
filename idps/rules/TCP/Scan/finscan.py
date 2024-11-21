from datetime import datetime
import time


def rule(packet, tcp_packets, db):
    """Règle Fin Scan:
    Un Fin Scan va envoyer des requêtes TCP avec le flag Fin
    Si le port est ouvert alors le serveur répondra pas
    Sinon le port est fermé et le serveur répondra: Reset ACK
    """
    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Vérification si nécessaire de récupérer les variables depuis la config
    if (rule.seuil == 0 and rule.time_window == 0):
        rule.time_window = db.get_key("finscan_time", 180)
        rule.seuil = db.get_key("finscan_count", 5)

    # Comptage du nombre de scan fin acceptés et refusés
    findeny_count = tcp_packets.count_packet_of_type(["F", "RA"], rule.time_window, True)
    finaccept_count = tcp_packets.count_packet_of_type(["F"], rule.time_window, True)

    if (findeny_count + finaccept_count >= rule.seuil):
        db.send_alert(datetime.now(), 5, None, "Fin scan", packet['IP'].src, packet['IP'].dst, proto="TCP", reason="Détection de nombreux patterns de Fin->Reset Ack et Fin->rien", act="Alerte")
        print(f"Alerte, seuil dépassés, risque de Fin Scan")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
