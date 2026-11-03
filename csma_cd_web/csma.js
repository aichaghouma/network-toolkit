const VITESSE_PROPAGATION = 2e8; // m/s, environ 2/3 de la vitesse de la lumière

function analyser({ debitMbps, distanceM, tailleOctets }) {
  for (const [nom, valeur] of Object.entries({ debitMbps, distanceM, tailleOctets })) {
    if (!Number.isFinite(valeur) || valeur <= 0) {
      throw new Error(`${nom} doit être un nombre strictement positif`);
    }
  }

  const debitBps = debitMbps * 1e6;
  const tailleBits = tailleOctets * 8;

  const tProp = distanceM / VITESSE_PROPAGATION;   // secondes
  const allerRetour = 2 * tProp;                   // secondes
  const tTrans = tailleBits / debitBps;            // secondes

  return {
    tPropUs: tProp * 1e6,
    allerRetourUs: allerRetour * 1e6,
    tTransUs: tTrans * 1e6,
    tailleMinBits: allerRetour * debitBps,
    tailleMinOctets: (allerRetour * debitBps) / 8,
    distanceMaxM: (VITESSE_PROPAGATION * tTrans) / 2,
    ok: tTrans >= allerRetour,
  };
}

if (typeof module !== "undefined") {
  module.exports = { analyser, VITESSE_PROPAGATION };
}
