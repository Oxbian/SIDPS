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
    event_gravite INT CHECK (event_gravite >= 0 AND event_gravite <= 10), -- Niveau de gravité de l'alerte sur une échelle de 0 à 10
    device_product VARCHAR(63), -- Nom du produit à l'origine de l'alerte
    device_vendor VARCHAR(63), -- Nom du fournisseur ou fabricant du produit
    device_version VARCHAR(31), -- Version du produit ou dispositif ayant généré l'alerte
    alerte_name VARCHAR(512), -- Nom descriptif de l'alerte
    destinationAddress VARCHAR(45), -- Adresse IP de destination impliquée dans l'alerte
    sourceAddress VARCHAR(45), -- Adresse IP source impliquée dans l'alerte
    destinationPort INT, -- Port de destination utilisé pour l'événement ou l'alerte
    sourcePort INT, -- Port source de l'événement ou de l'alerte
    protocol VARCHAR(10), -- Protocole réseau impliqué (ex : TCP, UDP)
    applicationProtocol VARCHAR(20), -- Protocole applicatif impliqué (ex : HTTP, FTP)
    reason TEXT, -- Description de la raison de l'alerte expliquant pourquoi elle a été générée
    action VARCHAR(50), -- Action entreprise en réponse à l'alerte (ex : bloqué, alerté uniquement, ...)
    commentaire TEXT -- Champ texte pour des notes ou commentaires additionnels concernant l'alerte
);
