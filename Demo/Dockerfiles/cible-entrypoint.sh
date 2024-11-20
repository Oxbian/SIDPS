#!/bin/sh

ip route add 172.20.1.0/24 via 172.20.2.2 dev eth0

# Lancer l'application IDPS
exec "$@"
