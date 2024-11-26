#/bin/sh
docker compose build
docker compose stop
#docker rm ids idps
docker rm attaquant1 attaquant2 ids idps cible alert_db web
docker compose up -d
