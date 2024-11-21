from datetime import datetime
import time


def rule(packet, tcp_packets, db):
    """
    Règle SYN Flood:
    Un SYN Flood va envoyer des requêtes TCP avec le flag SYN en très grand nombre afin de surcharger le serveur ou la cible
    - Si le port est ouvert, le serveur répond avec: SYN-ACK, puis le client RESET la connexion.
    - Si le port est fermé, le serveur répond avec: RST-ACK.
    """

    # Ne pas réagir si dans la période de cooldown
    if (rule.cooldown + rule.time_window > time.time()):
        return

    # Initialisation des paramètres à partir de la configuration si nécessaire
    if (rule.seuil == 0 and rule.time_window == 0):
        rule.time_window = db.get_key("synsflood_time", 60)
        rule.seuil = db.get_key("synflood_count", 100)

    # Comptage des paquets TCP correspondant aux motifs spécifiques
    syndeny_count = tcp_packets.count_packet_of_type(["S", "RA"], rule.time_window, True)
    synaccept_count = tcp_packets.count_packet_of_type(["S", "SA", "R"], rule.time_window, True)

    # Détection si le seuil est dépassé
    if (syndeny_count + synaccept_count >= rule.seuil):
        db.send_alert(datetime.now(), 5, None, "Syn flood", packet['IP'].src, packet['IP'].dst, proto="TCP", reason="Détection de nombreux patterns de Syn->SynACK->Reset et Syn->Reset ACK", act="Alerte")
        print("Alerte, seuil dépassé, risque de Syn Flood détecté.")
        rule.cooldown = time.time()


# Variables statiques
rule.cooldown = 0
rule.time_window = 0
rule.seuil = 0
