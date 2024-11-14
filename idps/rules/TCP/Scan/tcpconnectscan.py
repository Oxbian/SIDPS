# Seuils
TIME_WINDOW = 180 # 180 secondes pour avoir X paquets
NB_SEUIL = 5


def rule(packet, tcp_packets):
    if (tcp_packets.count_packet_of_type("A", TIME_WINDOW) + tcp_packets.count_packet_of_type("RA", TIME_WINDOW)) >= NB_SEUIL:
            print(f"Alerte, seuils dépassés, risque de TCPConnectScan")
