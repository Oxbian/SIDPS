CREATE DATABASE IF NOT EXISTS sidps DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'sidps'@'%' IDENTIFIED BY 'SUPERPASSWORD';
GRANT ALL PRIVILEGES ON sidps.* TO 'sidps'@'%';
FLUSH PRIVILEGES;
use sidps;

#-----------------------------------------------
# Nettoyage des tables dans la base de données
#-----------------------------------------------

DROP TABLE IF EXISTS alertes;

#-----------------------------------------------
# Table: alertes
#----------------------------------------------

CREATE TABLE alertes (
    id SERIAL PRIMARY KEY, -- Identifiant unique pour chaque alerte
    cef_version VARCHAR(10) DEFAULT 'CEF:1', -- Version du format CEF utilisé
    date_alerte TIMESTAMP(3) NOT NULL, -- Date et heure de l'alerte avec une précision de millisecondes
    agent_severity INT CHECK (agent_severity >= 0 AND agent_severity <= 10), -- Niveau de gravité de l'alerte sur une échelle de 0 à 10
	device_event_class_id VARCHAR(1023), -- Identifiant de la signature permettant d'aider les moteurs de corrélations
    device_product VARCHAR(63), -- Nom du produit à l'origine de l'alerte
    device_vendor VARCHAR(63), -- Nom du fournisseur ou fabricant du produit
    device_version VARCHAR(31), -- Version du produit ou dispositif ayant généré l'alerte
    name VARCHAR(512), -- Nom descriptif de l'alerte
	dst VARCHAR(45), -- Adresse IP de destination impliquée dans l'alerte
	src VARCHAR(45), -- Adresse IP source impliquée dans l'alerte
   	dpt INT, -- Port de destination utilisé pour l'événement ou l'alerte
    spt INT, -- Port source de l'événement ou de l'alerte
	msg VARCHAR(1023), -- Champ texte pour des notes ou commentaires additionnels concernant l'alerte
	proto VARCHAR(10), -- Protocole réseau impliqué (ex : TCP, UDP)
	bytesin INT, -- Quantité de bits entrant (cas de flood ou DOS)
	bytesout INT, -- Quantité des bits sortants
    reason VARCHAR(1023), -- Description de la raison de l'alerte expliquant pourquoi elle a été générée
    act VARCHAR(50) -- Action entreprise en réponse à l'alerte (ex : bloqué, alerté uniquement, ...)
);
