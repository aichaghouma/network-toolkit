def ip_to_int(ip: str) -> int:
    """'192.168.1.70' -> entier de 32 bits."""
    parts = ip.split(".")
    # 1. vérifier qu'il y a 4 morceaux
    if len(parts) != 4:
        raise ValueError("Adresse IPv4 invalide : 4 octets attendus")
    valeur = 0
    # 2. pour chaque morceau : vérifier 0 <= octet <= 255
    for p in parts:
        octet = int(p)
        if not 0 <= octet <= 255:
            raise ValueError(f"Octet invalide : {octet}")
        # 3. valeur = (valeur << 8) | octet
        valeur = (valeur << 8) | octet
    # 4. retourner valeur
    return valeur


def int_to_ip(valeur: int) -> str:
    """3232235846 -> '192.168.1.70'"""
    octet1 = (valeur >> 24) & 255
    octet2 = (valeur >> 16) & 255
    octet3 = (valeur >> 8) & 255
    octet4 = valeur & 255
    return ".".join(str(o) for o in (octet1, octet2, octet3, octet4))


def prefix_to_mask(prefixe: int) -> int:
    """24 -> entier du masque 255.255.255.0"""
    if not 0 <= prefixe <= 32:
        raise ValueError("Préfixe invalide : 0 à 32 attendu")
    return (0xFFFFFFFF << (32 - prefixe)) & 0xFFFFFFFF


def network_address(ip: int, masque: int) -> int:
    """Adresse réseau = ip ET masque"""
    return ip & masque


def broadcast_address(ip: int, masque: int) -> int:
    """Broadcast = adresse réseau OU inverse du masque"""
    return (ip & masque) | (~masque & 0xFFFFFFFF)


def first_host(reseau: int) -> int:
    """Première machine = adresse réseau + 1"""
    return reseau + 1


def last_host(broadcast: int) -> int:
    """Dernière machine = broadcast - 1"""
    return broadcast - 1


def host_count(prefixe: int) -> int:
    """Nombre de machines = 2^(32 - préfixe) - 2"""
    return max(0, 2 ** (32 - prefixe) - 2)


def calculer(cidr: str) -> dict:
    """'192.168.1.70/26' -> dictionnaire avec tous les résultats"""
    if "/" not in cidr:
        raise ValueError("Format attendu : adresse/préfixe, ex. 192.168.1.70/26")
    adresse, prefixe_texte = cidr.split("/")
    prefixe = int(prefixe_texte)

    ip = ip_to_int(adresse)
    masque = prefix_to_mask(prefixe)
    reseau = network_address(ip, masque)
    bcast = broadcast_address(ip, masque)

    return {
        "adresse": int_to_ip(ip),
        "prefixe": prefixe,
        "masque": int_to_ip(masque),
        "reseau": int_to_ip(reseau),
        "broadcast": int_to_ip(bcast),
        "premiere": int_to_ip(first_host(reseau)),
        "derniere": int_to_ip(last_host(bcast)),
        "hotes": host_count(prefixe),
    }


def afficher(cidr: str) -> None:
    """Affiche le résultat de calculer() de façon lisible"""
    r = calculer(cidr)
    print(f"Adresse        : {r['adresse']}/{r['prefixe']}")
    print(f"Masque         : {r['masque']}")
    print(f"Réseau         : {r['reseau']}")
    print(f"Broadcast      : {r['broadcast']}")
    print(f"Première hôte  : {r['premiere']}")
    print(f"Dernière hôte  : {r['derniere']}")
    print(f"Nombre d'hôtes : {r['hotes']}")
