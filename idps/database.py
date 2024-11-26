import mysql.connector


class Database:
    """Classe pour effectuer les actions liées à la base de données (envoi d'alertes...)"""

    def __init__(self, config):
        """Connexion à la base de données à partir des identifiants dans la config"""
        self.conn = mysql.connector.connect(host=config["db_host"], database=config["db_database"], user=config["db_user"], password=config["db_password"], port=config["db_port"])
        self.config = config

    def send_alert(self, date_alert = None, agent_severity = None, device_event_class_id = None, 
                   name = None, src = None, dst = None, dpt = None, spt = None, msg = None,
                   proto = None, bytesin = None, bytesout = None, reason = None, act = None):
        """Ajoute une alerte dans la base de données
        @param date_alert: Timestamp de l'alerte
        @param agent_severity: Criticité de l'alerte (0 - 10)
        @param device_event_class_id: Identifiant de signature, pour le moteur de corrélation
        @param name: Nom descriptif de l'alerte
        @param src: Adresse IP source
        @param dst: Adresse IP destination
        @param dpt: Port de destination
        @param spt: Port source
        @param msg: Champ de texte pour des notes ou commentaires additionnels
        @param proto: Protocol couche 4 (réseau) utilisé
        @param bytesin: Quantité de bytes (8 bits ici) entrants
        @param bytesout: Quantité de bytes (8 bits ici) sortants
        @param reason: Description de la raison de l'alerte
        @param act: Action prise en réponse de l'alerte
        """

        try:
            cursor = self.conn.cursor()
            sql_query = """
            INSERT INTO alertes (
                cef_version, date_alerte, agent_severity, device_event_class_id,
                device_product, device_vendor, device_version, name, dst, src,
                dpt, spt, msg, proto, bytesin, bytesout, reason, act
            ) VALUES (
                %(cef_version)s, %(date_alerte)s, %(agent_severity)s, %(device_event_class_id)s,
                %(device_product)s, %(device_vendor)s, %(device_version)s, %(name)s, %(dst)s, 
                %(src)s, %(dpt)s, %(spt)s, %(msg)s, %(proto)s, %(bytesin)s, %(bytesout)s,
                %(reason)s, %(act)s
            );
            """

            # Paramètres pour la requête SQL
            params = {
                "cef_version": self.config.get("cef_version", 1),
                "date_alerte": date_alert,
                "agent_severity": agent_severity,
                "device_event_class_id": device_event_class_id,
                "device_product": self.config.get("device_product", "SIDPS"),
                "device_vendor": self.config.get("device_vendor", "ArKa"),
                "device_version": self.config.get("device_version", "vAlpha"),
                "name": name,
                "src": src,
                "dst": dst,
                "dpt": dpt,
                "spt": spt,
                "msg": msg,
                "proto": proto,
                "bytesin": bytesin,
                "bytesout": bytesout,
                "reason": reason,
                "act": act
            }

            # Exécution de la requête d'insertion
            cursor.execute(sql_query, params)
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Erreur lors de l'envoi de l'alerte: {}".format(err))
