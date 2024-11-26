import importlib.util
import os
import time
import tcp
import database
import json
import protection

from scapy.all import sniff, TCP, IP
from scapy.config import conf
conf.debug_dissector = 2


def check_frame_w_rules(packet, rules_functions, objets):
    """Appliquer chaque règle des fonctions au paquet capturé.
    @param packet: Paquet actuel à analyser
    @param rules_functions: liste de fonctions de règles
    @param objets: Dictionnaire contenant le dictionnaire de config, la liste des paquets tcp précédents,
    la db, et le gestionnaire de règles Iptables"""

    for rule_func in rules_functions:
        try:
            rule_func(packet, objets)
        except Exception as e:
            print(f"Erreur lors de l'exécution de la règle : {e}")


def packet_callback(packet, rules_functions, objets):
    """Callback réception d'un paquet
    @param packet: Paquet actuel à classer
    @param rules_functions: liste des fonctions de règles
    @param objets: Dictionnaire contenant le dictionnaire de config, la liste des paquets tcp précédents,
    la db, et le gestionnaire de règles Iptables"""

    # Nettoyage des règles et paquets TCP dépassé
    objets["iptables_manager"].del_rules()
    objets["tcp_packets"].clean_old_packets()

    if IP in packet and TCP in packet:
        packet_origin = objets["tcp_packets"].add_packet(packet[IP].src, packet[TCP].sport, packet[IP].dst, packet[TCP].dport, packet[TCP].flags, time.time())

        # Stockage du paquet originel lié à ce paquet pour identifier la provenance de l'attaque
        objets['pkt_origin'] = packet_origin

        check_frame_w_rules(packet, rules_functions['TCP'], objets)


def load_rules(rules_dirpath = "/app/idps/rules"):
    """Charger les fonctions de règles du répertoire de règles et des sous répertoires
    @param rules_dirpath: Répertoire contenant les fichiers python de règles
    """

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
            raise PermissionError(f"Permission refusée pour accéder au répertoire: {current_dir}")
        except OSError as e:
            raise OSError(f"Erreur lors de l'accès au répertoire {current_dir}: {e}")

    return rules_functions


def read_config(config_filepath='config.json'):
    """Charge les configurations depuis le fichier de config"""

    try:
        with open(config_filepath, 'r', encoding='utf-8') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier JSON {config_filepath} n'a pas été trouvé.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Erreur lors de la lecture du fichier JSON. Le format peut être incorrect.")


def start_idps():
    """Charge les règles et démarre l'IDPS"""

    print("Récupération des configurations")
    config = read_config()
    print("Configurations chargées")

    print("Chargement des règles...")
    rules_functions = load_rules(config["rules_dirpath"])
    print("Les règles sont chargées")

    print("Connexion à la base de données")
    db = database.Database(config)
    print("Connexion réussite à la base de données")

    tcp_packets = tcp.TCP(300)
    protection_system = protection.Protection(config["protection"])

    objets = {"config": config, "database": db, "tcp_packets": tcp_packets, "iptables_manager": protection_system}

    # Lancer scapy & envoyer le paquet à chaque règle de l'IDPS
    sniff(iface=config["ifaces"], prn=lambda packet: packet_callback(packet, rules_functions, objets), store=0)


def main():
    print("Démarrage de l'IDPS")
    start_idps()


if __name__ == "__main__":
    main()
