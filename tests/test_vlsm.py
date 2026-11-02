import unittest

from subnet_calculator.vlsm import (
    prefix_for_hosts,
    plan_vlsm,
    verifier_chevauchement,
)

BESOINS = [("LAN D", 10), ("LAN A", 100), ("LAN C", 20), ("LAN B", 50)]


class TestPrefixForHosts(unittest.TestCase):
    def test_valeurs(self):
        attendu = {100: 25, 50: 26, 20: 27, 10: 28, 2: 30, 1: 30, 254: 24, 255: 23}
        for hotes, prefixe in attendu.items():
            self.assertEqual(prefix_for_hosts(hotes), prefixe)

    def test_invalide(self):
        with self.assertRaises(ValueError):
            prefix_for_hosts(0)


class TestPlanVlsm(unittest.TestCase):
    def test_ordre_et_reseaux(self):
        plan = plan_vlsm("192.168.1.0/24", BESOINS)
        self.assertEqual([s["nom"] for s in plan], ["LAN A", "LAN B", "LAN C", "LAN D"])
        self.assertEqual(
            [f"{s['reseau']}/{s['prefixe']}" for s in plan],
            ["192.168.1.0/25", "192.168.1.128/26", "192.168.1.192/27", "192.168.1.224/28"],
        )

    def test_plages_hotes(self):
        plan = plan_vlsm("192.168.1.0/24", BESOINS)
        self.assertEqual(plan[0]["premiere"], "192.168.1.1")
        self.assertEqual(plan[0]["derniere"], "192.168.1.126")
        self.assertEqual(plan[3]["premiere"], "192.168.1.225")
        self.assertEqual(plan[3]["derniere"], "192.168.1.238")
        self.assertEqual(plan[3]["disponibles"], 14)

    def test_sans_chevauchement(self):
        plan = plan_vlsm("192.168.1.0/24", BESOINS)
        blocs = [f"{s['reseau']}/{s['prefixe']}" for s in plan]
        self.assertEqual(verifier_chevauchement(blocs), [])

    def test_espace_insuffisant(self):
        with self.assertRaises(ValueError):
            plan_vlsm("192.168.1.0/24", [("LAN A", 200), ("LAN B", 100)])


class TestChevauchement(unittest.TestCase):
    def test_aucun_conflit(self):
        blocs = ["192.168.1.0/25", "192.168.1.128/26", "192.168.1.192/27"]
        self.assertEqual(verifier_chevauchement(blocs), [])

    def test_conflit_detecte(self):
        blocs = ["192.168.1.0/25", "192.168.1.64/26"]
        self.assertEqual(
            verifier_chevauchement(blocs),
            [("192.168.1.0/25", "192.168.1.64/26")],
        )


if __name__ == "__main__":
    unittest.main()
