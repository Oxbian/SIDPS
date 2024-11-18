def rule(packet, tcp_packets, db):
    """Règle SYNScan:
    Un SYNScan va envoyer des requêtes TCP avec le flag SYN
    Si le port est ouvert alors le serveur répondra: Syn ACK, puis le client Reset la connexion
    Sinon le port est fermé et le serveur répondera: Reset ACK
    """

    time_window = db.get_key("synscan_time", 180)
    seuil = db.get_key("synscan_count", 5)

    if (tcp_packets.count_packet_of_type("RA", time_window) + tcp_packets.count_packet_of_type("SA", time_window)) + tcp_packets.count_packet_of_type("R", time_window) >= seuil:
        print(f"Alerte, seuil dépassés, risque de SynScan")
