from scapy.all import sniff, TCP, IP
from scapy.config import conf
conf.debug_dissector = 2
import importlib.util
import os
import time
import tcp


def load_rules(rules_dirpath = "/app/idps/rules"):
    """Charger les fonctions de règles du répertoire de règles et des sous répertoires"""

    if not os.path.exists(rules_dirpath):
        raise ValueError(f"Le chemin spécifié n'existe pas: {rules_dirpath}")

    if not os.path.isdir(rules_dirpath):
        raise ValueError(f"Le chemin spécifié n'est pas un répertoire: {rules_dirpath}")

    rules_functions = {}
    # Liste de répertoires à explorer
    dirs_to_explore = [rules_dirpath]

    # Explorer chaque répertoire / sous répertoire à la rechercher de fichier de règles
    while dirs_to_explore:
        current_dir = dirs_to_explore.pop()

        try:
            for entry in os.scandir(current_dir):
                # Ignorer les liens symboliques
                if entry.is_symlink():
                    continue

                # Ajouter les répertoires dans la liste à explorer
                if entry.is_dir():
                    dirs_to_explore.append(entry.path)
                elif entry.is_file() and entry.name.endswith(".py"):
                    # Suppression de l'extension .py
                    module_name = entry.name[:-3]

                    # Déterminer le protocole à partir du répertoire parent
                    if "TCP" in entry.path:
                        parent_dir = "TCP"
                    else:
                        parent_dir = "WTF"

                    if parent_dir not in rules_functions:
                        rules_functions[parent_dir] = []

                    # Chargement du module
                    spec = importlib.util.spec_from_file_location(module_name, entry.path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Vérification que le module possède bien la fonction rule
                    if hasattr(module, "rule"):
                        rules_functions[parent_dir].append(module.rule)

        except PermissionError:
            print(f"Permission refusée pour accéder au répertoire: {current_dir}")
        except OSError as e:
            print(f"Erreur lors de l'accès au répertoire {current_dir}: {e}")

    return rules_functions


def check_frame_w_rules(packet, rules_functions, packets):
    """Appliquer chaque règle des fonctions au paquet capturé."""

    for rule_func in rules_functions:
        try:
            rule_func(packet, packets)
        except Exception as e:
            print(f"Erreur lors de l'exécution de la règle : {e}")


def packet_callback(packet, rules_functions, tcp_packets):
    #print(packet)
    if IP in packet and TCP in packet:
        tcp_packets.add_packet(packet[IP].src, packet[TCP].sport, packet[IP].dst, packet[TCP].dport, packet[TCP].flags, time.time())
        #print(tcp_packets[packet[IP].src])
        check_frame_w_rules(packet, rules_functions['TCP'], tcp_packets)
        tcp_packets.clean_old_packets()


def start_idps(IDS_IFACES = ["eth0","eth1"]):
    """Charge les règles et démarre l'IDPS"""
    print(f"Chargement des règles...")
    rules_functions = load_rules()
    print(f"Les règles sont chargées")

    # Opti possible: charger les règles par protocole, permettant des filtrages et donc optimiser
    # le nombre de fonctions vérifiant le paquet (snort s'arrête à la première corrélation par exemple)

    tcp_packets = tcp.TCP(300)

    # Lancer scapy & envoyer le paquet à chaque règle de l'IDPS
    sniff(iface=IDS_IFACES, prn=lambda packet: packet_callback(packet, rules_functions, tcp_packets), store=0)
    #wrpcap("idps.pcap", capture)


def main():
    print(f"Démarrage de l'IDPS")
    start_idps()
    print(f"IDPS opérationel")


if __name__ == "__main__":
    main()
