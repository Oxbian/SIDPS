import mysql.connector


class Database:
    """Classe pour effectuer les actions liées à la base de données (envoi d'alertes...)"""

    def __init__(self, config):
        """Connexion à la base de données à partir des identifiants dans la config"""
        self.conn = mysql.connector.connect(host=config["db_host"], database=config["db_database"], user=config["db_user"], password=config["db_password"], port=config["db_port"])
        self.config = config

    def send_alert(self, alert):
        """Ajoute une alerte dans la base de données
        @param alert: Alerte à rajouter dans la BDD"""

        try:
            cursor = self.conn.cursor()
            sql_query = """
            INSERT INTO alertes (
                cef_version, date_alerte, event_gravite, device_product,
                device_vendor, device_version, alerte_name, sourceAddress,
                destinationAddress, destinationPort, sourcePort, protocol,
                applicationProtocol, reason, action, commentaire
            ) VALUES (
                %(cef_version)s, %(date_alerte)s, %(event_gravite)s, %(device_product)s,
                %(device_vendor)s, %(device_version)s, %(alerte_name)s, %(src)s,
                %(dst)s, %(destinationPort)s, %(sourcePort)s, %(protocol)s,
                %(applicationProtocol)s, %(reason)s, %(action)s, %(commentaire)s
            );
            """

            # Paramètres pour la requête SQL
            params = {
                "cef_version": alert["CEF"],
                "date_alerte": alert["datetime"],
                "event_gravite": alert["agent_severity"],
                "device_product": alert["Device Product"],
                "device_vendor": alert["Device Vendor"],
                "device_version": alert["Device Version"],
                "alerte_name": alert["name"],
                "src": alert["src"],
                "dst": alert["dst"],
                "destinationPort": alert["dstPort"],
                "sourcePort": alert["srcPort"],
                "protocol": alert["protocol"],
                "applicationProtocol": alert["applicationProtocol"],
                "reason": alert["reason"],
                "action": alert["action"],
                "commentaire": alert["commentaire"]
            }

            # Exécution de la requête d'insertion
            cursor.execute(sql_query, params)
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Erreur lors de l'envoi de l'alerte: {}".format(err))

    def get_key(self, key, default_val):
        """Donne le contenue d'un paramètre spécifique de la config
        @param key: clé du paramètre souhaité
        @param default_val: valeur par défaut si la clé n'existe pas"""

        return self.config.get(key, None)
