const MAX_TENTATIVES = 16;
const PLAFOND_EXPOSANT = 10;

// Nombre de créneaux à attendre après `collisions` collisions consécutives.
function backoffSlots(collisions, rng = Math.random) {
  if (!Number.isInteger(collisions) || collisions < 1) {
    throw new Error("collisions doit être un entier >= 1");
  }
  if (collisions >= MAX_TENTATIVES) {
    throw new Error("Trame abandonnée : trop de collisions");
  }
  const exposant = Math.min(collisions, PLAFOND_EXPOSANT);
  return Math.floor(rng() * 2 ** exposant); // entier entre 0 et 2^exposant - 1
}

class Station {
  constructor(nom, nbTrames) {
    this.nom = nom;
    this.tramesRestantes = nbTrames;
    this.collisions = 0;   // collisions consécutives pour la trame en cours
    this.attente = 0;      // créneaux à attendre avant de ré-émettre
    this.envoyees = 0;
    this.abandonnees = 0;
  }

  // Elle émet si elle a des trames et n'est plus en attente.
  veutEmettre() {
    return this.tramesRestantes > 0 && this.attente === 0;
  }

  attendreUnCreneau() {
    if (this.attente > 0) {
      this.attente -= 1;
    }
  }

  // Émission réussie : la trame est partie.
  succes() {
    this.tramesRestantes -= 1;
    this.envoyees += 1;
    this.collisions = 0;
  }

  // Collision : backoff, ou abandon de la trame après 16 collisions.
  collision(rng = Math.random) {
    this.collisions += 1;
    if (this.collisions >= MAX_TENTATIVES) {
      this.tramesRestantes -= 1;
      this.abandonnees += 1;
      this.collisions = 0;
      this.attente = 0;
      return "abandon";
    }
    this.attente = backoffSlots(this.collisions, rng);
    return "backoff";
  }
}

if (typeof module !== "undefined") {
  module.exports = { backoffSlots, Station, MAX_TENTATIVES, PLAFOND_EXPOSANT };
}
