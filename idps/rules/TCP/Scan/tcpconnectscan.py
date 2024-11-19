from datetime import datetime

def rule(packet, tcp_packets, db):
    """Règle TCPConnect Scan:
    Un scan TCP connect va effectuer une connexion TCP en entier sur chaque port scanné.
    Si le port est ouvert le serveur acceptera la connexion SYN -> SYN ACK -> ACK -> Reset -> ACK
    Sinon le port est fermé et le serveur refusera la connexion SYN -> Reset ACK
    """
    time_window = db.get_key("tcpconnectscan_time", 180)
    seuil = db.get_key("tcpconnectscan_count", 5)

    if (tcp_packets.count_packet_of_type("A", time_window) + tcp_packets.count_packet_of_type("RA", time_window)) >= seuil:
        db.send_alert(datetime.now(), 5, None, "TCPConnect Scan", packet['IP'].src, packet['IP'].dst, proto="TCP", reason="Détection de nombreux patterns de Syn->SynACK->ACK->Reset->ACK et Syn->Reset ACK", act="Alerte") 
        print(f"Alerte, seuils dépassés, risque de TCPConnectScan")
