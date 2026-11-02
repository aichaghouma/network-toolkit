import sys

from subnet_calculator.core import afficher
from subnet_calculator.vlsm import afficher_plan

USAGE = """Usage :
  python3 main.py <adresse/préfixe>
  python3 main.py vlsm <réseau/préfixe> "<nom>=<machines>" ...

Exemples :
  python3 main.py 192.168.1.70/26
  python3 main.py vlsm 192.168.1.0/24 "LAN A=100" "LAN B=50" "LAN C=20"
"""


def lire_besoins(arguments: list) -> list:
    besoins = []
    for texte in arguments:
        if "=" not in texte:
            raise ValueError(f"Besoin invalide : '{texte}' (format attendu : nom=machines)")
        nom, nombre = texte.rsplit("=", 1)
        besoins.append((nom.strip(), int(nombre)))
    return besoins


def main() -> None:
    args = sys.argv[1:]
    try:
        if len(args) == 1:
            afficher(args[0])
        elif len(args) >= 3 and args[0] == "vlsm":
            afficher_plan(args[1], lire_besoins(args[2:]))
        else:
            print(USAGE)
            sys.exit(1)
    except ValueError as erreur:
        print(f"Erreur : {erreur}")
        sys.exit(1)


if __name__ == "__main__":
    main()
