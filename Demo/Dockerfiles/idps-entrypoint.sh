#!/bin/sh

# Activer l'acheminement des paquets
echo 1 > /proc/sys/net/ipv4/ip_forward

# Configurer les règles iptables
ip route add 172.20.2.0/24 via 172.20.2.2 dev eth1
ip route add 172.20.1.0/24 via 172.20.1.3 dev eth2

iptables -A FORWARD -i eth1 -o eth2 -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -j ACCEPT

# Lancer l'application IDPS
exec "$@"
