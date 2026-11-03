const { analyser } = require("./csma.js");
const { Station } = require("./simulateur.js");
const { simuler, afficherJournal } = require("./moteur.js");

// Partie 1 : CSMA/CD est-il possible avec ces paramètres ?
const params = { debitMbps: 10, distanceM: 2500, tailleOctets: 64 };
const r = analyser(params);
console.log(`Débit ${params.debitMbps} Mbit/s, distance ${params.distanceM} m, trame ${params.tailleOctets} octets`);
console.log(`  Propagation          : ${r.tPropUs.toFixed(1)} µs`);
console.log(`  Aller-retour         : ${r.allerRetourUs.toFixed(1)} µs`);
console.log(`  Émission de la trame : ${r.tTransUs.toFixed(1)} µs`);
console.log(`  Taille minimale      : ${r.tailleMinOctets.toFixed(2)} octets`);
console.log(`  Distance maximale    : ${r.distanceMaxM.toFixed(0)} m`);
console.log(`  CSMA/CD fonctionne   : ${r.ok ? "oui" : "non"}`);

// Partie 2 : deux stations, hasard fixé pour un résultat reproductible
console.log("\nSimulation : 2 stations, 1 trame chacune");
let i = 0;
const rng = () => [0, 0.99][i++ % 2];
afficherJournal(simuler([new Station("A", 1), new Station("B", 1)], { rng }));
