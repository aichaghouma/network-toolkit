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

## 2. Générateur de plan VLSM

À partir d'un réseau de départ et d'une liste de besoins, le programme trie les besoins du plus grand au plus petit, calcule le plus petit bloc adapté à chacun et affiche le plan d'adressage. Il signale aussi un espace insuffisant.

### Utilisation

```bash
python3 main.py vlsm 192.168.1.0/24 "LAN A=100" "LAN B=50" "LAN C=20" "LAN D=10"
```

Résultat (extrait) :

```
LAN A (100 machines demandées)
  Réseau    : 192.168.1.0/25  (masque 255.255.255.128)
  Hôtes     : 192.168.1.1 -> 192.168.1.126
  Broadcast : 192.168.1.127

LAN B (50 machines demandées)
  Réseau    : 192.168.1.128/26  (masque 255.255.255.192)
  Hôtes     : 192.168.1.129 -> 192.168.1.190
  Broadcast : 192.168.1.191
```

Si le réseau est trop petit :

```
Erreur : Espace insuffisant dans 192.168.1.0/24 pour 'LAN B' (100 machines)
```

## 3. Simulateur CSMA/CD (JavaScript)

CSMA/CD est le protocole d'accès de l'Ethernet partagé : une station écoute le câble avant d'émettre (Carrier Sense) et détecte les collisions pendant l'émission (Collision Detection). Cette partie est écrite en JavaScript (Node.js) et comporte deux volets :

- un calcul qui indique si CSMA/CD est possible pour un débit, une distance et une taille de trame donnés ;
- une simulation créneau par créneau de plusieurs stations qui partagent le même câble, avec le backoff exponentiel binaire.

### Utilisation

```bash
node csma_cd_web/demo.js
```

Résultat :

```
Débit 10 Mbit/s, distance 2500 m, trame 64 octets
  Propagation          : 12.5 µs
  Aller-retour         : 25.0 µs
  Émission de la trame : 51.2 µs
  Taille minimale      : 31.25 octets
  Distance maximale    : 5120 m
  CSMA/CD fonctionne   : oui

Simulation : 2 stations, 1 trame chacune
Créneau 1 : collision [A, B]
Créneau 2 : succes [A]
Créneau 3 : succes [B]
Créneaux : 3 | succès : 2 | collisions : 1 | libres : 0 | abandons : 0 | utilisation : 67 %
```

### Comment ça marche

Le calcul (`csma.js`) vérifie que l'émetteur émet encore quand l'écho d'une collision lui revient :

- temps de propagation = distance / vitesse du signal (environ 2×10^8 m/s)
- aller-retour = 2 × temps de propagation
- temps d'émission = taille de la trame (en bits) / débit
- condition : temps d'émission >= aller-retour
- taille minimale de trame = aller-retour × débit ; distance maximale = vitesse × temps d'émission / 2

La simulation (`simulateur.js` et `moteur.js`) avance créneau par créneau :

- une seule station qui émet : succès ;
- deux stations ou plus : collision, puis chaque station attend un nombre de créneaux tiré au hasard entre 0 et 2^n - 1 après n collisions (plafond à n = 10) ;
- après 16 collisions consécutives, la trame est abandonnée ;
- à la fin, le programme affiche le journal et des statistiques (succès, collisions, abandons, taux d'utilisation).

### Fichiers de la partie 3

- `csma_cd_web/csma.js` : formules de propagation, taille minimale et distance maximale
- `csma_cd_web/simulateur.js` : backoff exponentiel binaire et classe `Station`
- `csma_cd_web/moteur.js` : boucle de simulation
- `csma_cd_web/demo.js` : exemple d'utilisation

### Prérequis

- Node.js (aucune bibliothèque externe)
