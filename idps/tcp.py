import time


class TCP:
    def __init__(self, clean_time=300):
        """Constructeur de la classe TCP
        @param clean_time: temps avant qu'un paquet soit nettoyé"""

        self.packets = {}
        self.clean_time = clean_time

    def add_packet(self, ip_src, port_src, ip_dst, port_dst, flags, timestamp):
        """Ajoute le suivi d'un paquet dans le dictionnaire"""

        timestamp = int(timestamp)

        # Initialisation de la liste de paquets pour l'IP source
        if ip_src not in self.packets:
            self.packets[ip_src] = []

        if flags == "S":
            self.packets[ip_src].append([port_src, ip_dst, port_dst, ["S"], timestamp])
            return

        elif flags is None:
            self.packets[ip_src].append([port_src, ip_dst, port_dst, [""], timestamp])
            return

        elif flags == "FPU":
            self.packets[ip_src].append([port_src, ip_dst, port_dst, ["FPU"], timestamp])
            return

        elif flags == "SA":
            i, ip = self.find_packet_to_replace(ip_src, port_src, ip_dst, port_dst, "S")

            if i is not None:
                #print(f"i: {i}, {ip_src}:{port_src}->{ip_dst}:{port_dst}, paquets: \n{self.packets}")
                self.packets[ip][i][3].append("SA")
                self.packets[ip][i][4] = timestamp
                return
            else:
                self.packets[ip_src].append([port_src, ip_dst, port_dst, ["SA"], timestamp])
                return

        elif flags == "A":
            i, ip = self.find_packet_to_replace(ip_src, port_src, ip_dst, port_dst, "SA")
            if i is None:
                i, ip = self.find_packet_to_replace(ip_src, port_src, ip_dst, port_dst, "R")

            if i is not None:
                #print(f"i: {i}, {ip_src}:{port_src}->{ip_dst}:{port_dst}, paquets: \n{self.packets}")
                self.packets[ip][i][3].append("A")
                self.packets[ip][i][4] = timestamp
                return
            else:
                self.packets[ip_src].append([port_src, ip_dst, port_dst, ["A"], timestamp])
                return

        elif flags == "RA":
            i, ip = self.find_packet_to_replace(ip_src, port_src, ip_dst, port_dst, "A")

            if i is None:
                i, ip = self.find_packet_to_replace(ip_src, port_src, ip_dst, port_dst, "S")

            if i is not None:
                #print(f"i: {i}, {ip_src}:{port_src}->{ip_dst}:{port_dst}, paquets: \n{self.packets}")
                self.packets[ip][i][3].append("RA")
                self.packets[ip][i][4] = timestamp
                return
            else:
                self.packets[ip_src].append([port_src, ip_dst, port_dst, ["RA"], timestamp])
                return

        elif flags == "R":
            i, ip = self.find_packet_to_replace(ip_src, port_src, ip_dst, port_dst, "A")

            if i is None:
                i, ip = self.find_packet_to_replace(ip_src, port_src, ip_dst, port_dst, "S")

            if i is not None:
                #print(f"i: {i}, {ip_src}:{port_src}->{ip_dst}:{port_dst}, paquets: \n{self.packets}")
                self.packets[ip][i][3].append("R")
                self.packets[ip][i][4] = timestamp
                return
            else:
                self.packets[ip_src].append([port_src, ip_dst, port_dst, ["R"], timestamp])
                return

        elif flags == "F":
            i, ip = self.find_packet_to_replace(ip_src, port_src, ip_dst, port_dst, "A")

            if i is not None:
                #print(f"i: {i}, {ip_src}:{port_src}->{ip_dst}:{port_dst}, paquets: \n{self.packets}")
                self.packets[ip][i][3].append("F")
                self.packets[ip][i][4] = timestamp
                return
            else:
                self.packets[ip_src].append([port_src, ip_dst, port_dst, ["F"], timestamp])
                return

        # TODO: ajout flag fin, none, fin urg push

    def find_packet_to_replace(self, ip_src, port_src, ip_dst, port_dst, flags):
        """Cherche l'indice et le port de source du paquet dont le flag doit être remplacé"""

        # Recherche dans le sens src->dst
        if ip_src in self.packets.keys():
            for i, [p_s, ip_d, p_d, f, stamp] in enumerate(self.packets[ip_src]):
                if p_s == port_src and ip_d == ip_dst and p_d == port_dst and flags in f:
                    return i, ip_src

        # Recherche dans le sens dst->src
        if ip_dst in self.packets.keys():
            for i, [p_d, ip_s, p_s, f, stamp] in enumerate(self.packets[ip_dst]):
                if p_s == port_src and ip_s == ip_src and p_d == port_dst and flags in f:
                    return i, ip_dst

        return None, None

    def clean_old_packets(self):
        """Supprime les paquets qui date de plus longtemps que le temps de clean"""
        current_timestamp = time.time()

        # Parcours chaque ip_source de la liste
        for ip_src in list(self.packets.keys()):

            # Vérification si le paquet doit être supprimé ou non
            i = 0
            while i < len(self.packets[ip_src]):
                packet = self.packets[ip_src][i]
                if packet[4] <= current_timestamp - self.clean_time:
                    del self.packets[ip_src][i]
                else:
                    i += 1

            # Suppression de la case de l'ip source si elle n'existe plus
            if not self.packets[ip_src]:
                del self.packets[ip_src]

    def count_packet_of_type(self, flag, time_treshold, isList = False):
        """Compte les paquets qui ont le flag choisi et qui sont dans la fenêtre de temps"""
        count = 0

        current_timestamp = time.time()
        for ip in list(self.packets.keys()):
            for packet in self.packets[ip]:
                if isList and set(flag) == set(packet[3]) and packet[4] >= current_timestamp - time_treshold:
                    count += 1
                elif not isList and flag in packet[3] and packet[4] >= current_timestamp - time_treshold:
                    count += 1
        return count

    def __getitem__(self, src_ip):
        """Retourne la liste des paquets liés à une adresse IP, pour du déboggage"""

        return self.packets.get(src_ip, None)
