# Seuils
TIME_WINDOW = 180
NB_SEUIL = 5


def rule(packet, tcp_packets):
    if (tcp_packets.count_packet_of_type("RA", TIME_WINDOW) + tcp_packets.count_packet_of_type("SA", TIME_WINDOW)) + tcp_packets.count_packet_of_type("R", TIME_WINDOW) >= NB_SEUIL:
        print(f"Alerte, seuil dépassés, risque de SynScan")
