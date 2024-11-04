# SIDPS - Simple Intrusion Detection and Protection System

SIDPS est un outils de détection et de prévention d'intrusion.  
Il est capable de détecter & d'identifier différents types d'attaques réseaux, ainsi que de protéger contre certaines de ces attaques automatiquement.  
  
**Attention, il s'agit d'un projet étudiant, dont le but est de réaliser une démonstration pour un projet Universitaire ! Ce projet ne sera probablement pas maintenu par la suite**

## Fonctionnalités clés:

- Rapidité
- Interface web simple et intuitive
- Messages d'alertes interopérable suivant la norme [CEF (Common Event Format)](https://www.microfocus.com/documentation/arcsight/arcsight-smartconnectors-8.4/pdfdoc/cef-implementation-standard/cef-implementation-standard.pdf)
- Détections de nombreuses attaques réseaux (scan, DOS, ...)

## Installation

Pour son fonctionnement, ce projet utilise une base de donnée [redis](https://redis.io/).  
  
Un moyen simple d'avoir une base de donnée redis fonctionnel est d'utilisé docker:  

```bash
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

Ou si vous souhaitez avoir une interface graphique pour Redis en plus de la base de donnée, vous pouvez installer un docker de [redis insight](https://redis.io/insight/).

```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

*Installation interface web & noyau de l'IDS*

## Structure de la base de données Redis

La base de données Redis est structurée de la façon suivante:  
- stream `logs:alertes` contenant toutes les alertes envoyés par le noyau de l'IDPS  
- stream `logs:correlations` contenant toutes les corrélations d'alertes, avec un message de corrélation et les alertes corrélées  
  
Ces deux streams suivent la norme CEF, mais sont structurées sous la forme d'objet et non d'une seule chaine de caractère. Afin de faciliter le parsing par la suite.  

## Interface de tests d'alertes

Un script python `tests/cef-generator.py` permet de générer des alertes CEF dans la base de données Redis.  
Ce script peut être utile pour le développement d'interface d'affichage des alertes. Pour l'utiliser il faut une base de donnée redis, et mettre les identifiants dans le script.  
De plus, ce script à besoin de la librairie `redis` pour pouvoir ajouter / faire des requêtes à la base de données Redis.  
  
Pour cela, utiliser les commandes suivantes:  

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Puis executer le script `tests/cef-generator.py` avec le python3 du l'environnement virtuel.

```bash
.venv/bin/python3 tests/cef-generator.py
```

## TODO

- Noyau d'analyse de l'IDS  
- Interface web pour visualiser les alertes / rechercher dedans  
- Moteur de corrélation des alertes (récupération + renvoi dans Redis). 
