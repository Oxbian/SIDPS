#!/bin/sh

ip route add 172.20.2.0/24 via 172.20.1.3 dev eth0

# Lancer l'application IDPS
exec "$@"
