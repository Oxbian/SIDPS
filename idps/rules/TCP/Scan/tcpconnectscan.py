def rule(packet, tcp_packets, db):
    """Règle TCPConnect Scan:
    Un scan TCP connect va effectuer une connexion TCP en entier sur chaque port scanné.
    Si le port est ouvert le serveur acceptera la connexion SYN -> SYN ACK -> ACK -> Reset -> ACK
    Sinon le port est fermé et le serveur refusera la connexion SYN -> Reset ACK
    """
    time_window = db.get_key("tcpconnectscan_time", 180)
    seuil = db.get_key("tcpconnectscan_count", 5)

    if (tcp_packets.count_packet_of_type("A", time_window) + tcp_packets.count_packet_of_type("RA", time_window)) >= seuil:
            print(f"Alerte, seuils dépassés, risque de TCPConnectScan")
