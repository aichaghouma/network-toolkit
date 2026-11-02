import unittest

from subnet_calculator.core import (
    ip_to_int,
    int_to_ip,
    prefix_to_mask,
    network_address,
    broadcast_address,
    host_count,
    calculer,
)


class TestConversion(unittest.TestCase):
    def test_ip_to_int(self):
        self.assertEqual(ip_to_int("192.168.1.70"), 3232235846)

    def test_int_to_ip(self):
        self.assertEqual(int_to_ip(3232235846), "192.168.1.70")

    def test_aller_retour(self):
        self.assertEqual(int_to_ip(ip_to_int("10.0.0.1")), "10.0.0.1")

    def test_ip_invalide(self):
        with self.assertRaises(ValueError):
            ip_to_int("192.168.1.300")
        with self.assertRaises(ValueError):
            ip_to_int("192.168.1")


class TestMasque(unittest.TestCase):
    def test_masque_24(self):
        self.assertEqual(int_to_ip(prefix_to_mask(24)), "255.255.255.0")

    def test_masque_26(self):
        self.assertEqual(int_to_ip(prefix_to_mask(26)), "255.255.255.192")

    def test_masque_limites(self):
        self.assertEqual(int_to_ip(prefix_to_mask(0)), "0.0.0.0")
        self.assertEqual(int_to_ip(prefix_to_mask(32)), "255.255.255.255")

    def test_prefixe_invalide(self):
        with self.assertRaises(ValueError):
            prefix_to_mask(33)


class TestReseau(unittest.TestCase):
    def test_reseau_et_broadcast(self):
        ip = ip_to_int("192.168.1.70")
        masque = prefix_to_mask(26)
        self.assertEqual(int_to_ip(network_address(ip, masque)), "192.168.1.64")
        self.assertEqual(int_to_ip(broadcast_address(ip, masque)), "192.168.1.127")

    def test_nombre_hotes(self):
        self.assertEqual(host_count(24), 254)
        self.assertEqual(host_count(26), 62)

    def test_calculer(self):
        r = calculer("172.16.5.130/20")
        self.assertEqual(r["reseau"], "172.16.0.0")
        self.assertEqual(r["broadcast"], "172.16.15.255")
        self.assertEqual(r["hotes"], 4094)


if __name__ == "__main__":
    unittest.main()
