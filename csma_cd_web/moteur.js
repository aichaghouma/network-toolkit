const { Station } = require("./simulateur.js");

// Lance la simulation et retourne le journal (créneau par créneau) et les statistiques.
function simuler(stations, { rng = Math.random, maxCreneaux = 10000 } = {}) {
  const journal = [];
  let creneau = 0;

  while (creneau < maxCreneaux && stations.some((s) => s.tramesRestantes > 0)) {
    creneau += 1;
    const emetteurs = stations.filter((s) => s.veutEmettre());
    let evenement;
    let abandons = [];

    if (emetteurs.length === 0) {
      evenement = "libre";
    } else if (emetteurs.length === 1) {
      emetteurs[0].succes();
      evenement = "succes";
    } else {
      const issues = emetteurs.map((s) => s.collision(rng));
      abandons = emetteurs.filter((_, i) => issues[i] === "abandon").map((s) => s.nom);
      evenement = "collision";
    }

    // Les stations qui n'ont pas émis laissent passer un créneau d'attente.
    stations
      .filter((s) => !emetteurs.includes(s))
      .forEach((s) => s.attendreUnCreneau());

    journal.push({ creneau, evenement, stations: emetteurs.map((s) => s.nom), abandons });
  }

  const compter = (type) => journal.filter((j) => j.evenement === type).length;
  const succes = compter("succes");
  const stats = {
    creneaux: creneau,
    succes,
    collisions: compter("collision"),
    libres: compter("libre"),
    abandonnees: stations.reduce((total, s) => total + s.abandonnees, 0),
    utilisation: creneau > 0 ? succes / creneau : 0,
  };
  return { journal, stats };
}

function afficherJournal({ journal, stats }) {
  for (const j of journal) {
    const noms = j.stations.join(", ") || "-";
    const extra = j.abandons.length > 0 ? " (abandon : " + j.abandons.join(", ") + ")" : "";
    console.log("Créneau " + j.creneau + " : " + j.evenement + " [" + noms + "]" + extra);
  }
  console.log(
    "Créneaux : " + stats.creneaux +
      " | succès : " + stats.succes +
      " | collisions : " + stats.collisions +
      " | libres : " + stats.libres +
      " | abandons : " + stats.abandonnees +
      " | utilisation : " + (stats.utilisation * 100).toFixed(0) + " %"
  );
}

if (typeof module !== "undefined") {
  module.exports = { simuler, afficherJournal };
}
