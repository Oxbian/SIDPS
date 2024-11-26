import subprocess
import time


class Protection:
    """Classe pour activer la protection du système avec iptables"""

    def __init__(self, activate = 0):
        """Initialisation de la protection avec une liste pour stockées les règles créer"""
        self.rules = []
        self.activate = int(activate)

    def add_rule(self, rule, duration):
        """Ajouter une règle dans iptables
        @param rule: Règle à ajouter
        @param duration: Durée d'execution de la règle"""

        print(f"Rule: {rule}, {duration}, {self.activate}")
        if self.activate == 0:
            return

        print("Rule run")
        try:
            subprocess.run(rule.split(' '), check=True)
            print(f"[iptables] Règle ajouter {rule}")
            self.rules.append([rule, time.time(), duration])
        except subprocess.CalledProcessError as e:
            print(f"[iptables] Erreur suppression de la règle {rule}: {e}")

    def del_rules(self):
        """Supprimer les règles obsolètes de l'iptables"""

        if self.activate is False:
            return

        curr = time.time()
        for i, elt in enumerate(self.rules, 0):
            if elt[1] + elt[2] <= curr:
                self.del_rule(self, elt[0].replace("-I", "-D"), i)

    def del_rule(self, rule, i):
        """Supprimer une règle dans iptables"""

        try:
            subprocess.run(rule.split(' '), check=True)
            print("[iptables] Règle supprimer {rule}")
            self.rules.pop(i)
        except subprocess.CalledProcessError as e:
            print(f"[iptables] Erreur suppression de la règle {rule}: {e}")
