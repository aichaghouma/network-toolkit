import sys

from subnet_calculator.core import afficher


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage : python3 main.py <adresse/préfixe>")
        print("Exemple : python3 main.py 192.168.1.70/26")
        sys.exit(1)

    try:
        afficher(sys.argv[1])
    except ValueError as erreur:
        print(f"Erreur : {erreur}")
        sys.exit(1)


if __name__ == "__main__":
    main()
