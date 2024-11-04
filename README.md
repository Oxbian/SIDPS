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

## TODO

- Choix du format d'enregistrement des données dans Redis
- Noyau d'analyse de l'IDS
- Interface web pour visualiser les alertes / rechercher dedans
- Moteur de corrélation des alertes (récupération + renvoi dans Redis). 
