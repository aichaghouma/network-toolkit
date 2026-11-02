from subnet_calculator.core import (
    ip_to_int,
    int_to_ip,
    prefix_to_mask,
    network_address,
    broadcast_address,
    first_host,
    last_host,
    host_count,
)


def prefix_for_hosts(hotes: int) -> int:
    """Plus petit bloc (plus grand préfixe) qui contient `hotes` machines."""
    if hotes < 1:
        raise ValueError("Le nombre de machines doit être au moins 1")
    for prefixe in range(30, -1, -1):
        if host_count(prefixe) >= hotes:
            return prefixe
    raise ValueError("Trop de machines pour un réseau IPv4")


def plan_vlsm(reseau_cidr: str, besoins: list) -> list:
    """
    reseau_cidr : '192.168.1.0/24'
    besoins     : [("LAN A", 100), ("LAN B", 50), ...]
    Retourne la liste des sous-réseaux, triés du plus grand au plus petit.
    """
    adresse, prefixe_texte = reseau_cidr.split("/")
    prefixe_depart = int(prefixe_texte)
    masque_depart = prefix_to_mask(prefixe_depart)
    debut = network_address(ip_to_int(adresse), masque_depart)
    fin = broadcast_address(debut, masque_depart)

    plan = []
    courant = debut
    for nom, hotes in sorted(besoins, key=lambda b: b[1], reverse=True):
        prefixe = prefix_for_hosts(hotes)
        taille = 2 ** (32 - prefixe)

        # le bloc doit commencer sur un multiple de sa taille
        if courant % taille != 0:
            courant += taille - (courant % taille)

        if courant + taille - 1 > fin:
            raise ValueError(
                f"Espace insuffisant dans {reseau_cidr} pour '{nom}' ({hotes} machines)"
            )

        masque = prefix_to_mask(prefixe)
        reseau = network_address(courant, masque)
        bcast = broadcast_address(courant, masque)
        plan.append({
            "nom": nom,
            "demandes": hotes,
            "prefixe": prefixe,
            "masque": int_to_ip(masque),
            "reseau": int_to_ip(reseau),
            "premiere": int_to_ip(first_host(reseau)),
            "derniere": int_to_ip(last_host(bcast)),
            "broadcast": int_to_ip(bcast),
            "disponibles": host_count(prefixe),
        })
        courant += taille
    return plan


def afficher_plan(reseau_cidr: str, besoins: list) -> None:
    """Affiche le plan d'adressage complet."""
    plan = plan_vlsm(reseau_cidr, besoins)
    print(f"Plan d'adressage pour {reseau_cidr}\n")
    for s in plan:
        print(f"{s['nom']} ({s['demandes']} machines demandées)")
        print(f"  Réseau    : {s['reseau']}/{s['prefixe']}  (masque {s['masque']})")
        print(f"  Hôtes     : {s['premiere']} -> {s['derniere']}")
        print(f"  Broadcast : {s['broadcast']}")
        print(f"  Disponibles : {s['disponibles']}\n")


def verifier_chevauchement(blocs: list) -> list:
    """
    blocs : liste de chaînes CIDR, ex. ['192.168.1.0/25', '192.168.1.64/26']
    Retourne la liste des paires qui se chevauchent.
    """
    intervalles = []
    for cidr in blocs:
        adresse, prefixe_texte = cidr.split("/")
        masque = prefix_to_mask(int(prefixe_texte))
        debut = network_address(ip_to_int(adresse), masque)
        fin = broadcast_address(debut, masque)
        intervalles.append((cidr, debut, fin))

    conflits = []
    for i in range(len(intervalles)):
        for j in range(i + 1, len(intervalles)):
            a, b = intervalles[i], intervalles[j]
            if a[1] <= b[2] and b[1] <= a[2]:
                conflits.append((a[0], b[0]))
    return conflits
