# Network Toolkit

Une collection d'outils réseau écrits en Python, réalisés pour mettre en pratique le cours de réseaux locaux TCP/IP.

## 1. Calculateur IPv4 / subnetting

À partir d'une adresse IPv4 et d'un préfixe (notation CIDR), le calculateur donne :

- le masque de sous-réseau
- l'adresse réseau
- l'adresse de broadcast
- la première et la dernière adresse utilisable
- le nombre d'hôtes

### Utilisation

```bash
python3 main.py 192.168.1.70/26
```

Résultat :

```
Adresse        : 192.168.1.70/26
Masque         : 255.255.255.192
Réseau         : 192.168.1.64
Broadcast      : 192.168.1.127
Première hôte  : 192.168.1.65
Dernière hôte  : 192.168.1.126
Nombre d'hôtes : 62
```

Autres exemples :

```bash
python3 main.py 10.0.0.1/8
python3 main.py 172.16.5.130/20
```

En cas d'entrée invalide (octet supérieur à 255, préfixe hors de 0 à 32, format incorrect), le programme affiche un message d'erreur clair.

### Comment ça marche

Le calcul se fait directement sur les bits :

- l'adresse est convertie en un entier de 32 bits (`ip_to_int`)
- le masque est construit à partir du préfixe (`prefix_to_mask`)
- adresse réseau = `ip & masque`
- broadcast = adresse réseau `|` inverse du masque
- nombre d'hôtes = 2^(32 - préfixe) - 2

### Structure du projet

```
network-toolkit/
├── main.py                  # point d'entrée en ligne de commande
├── README.md
└── subnet_calculator/
    ├── __init__.py
    └── core.py              # fonctions de calcul
```

## Prérequis

- Python 3
- aucune bibliothèque externe
