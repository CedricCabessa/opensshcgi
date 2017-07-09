#!/usr/bin/python3

import unittest
from openssh import check_addr

class TestCheckAddr(unittest.TestCase):
    def test_check_addr(self):
        self.assertEquals(check_addr("192.168.0.5"), "192.168.0.5/32")
        self.assertEquals(check_addr("192.168.0.5/24"), "192.168.0.0/24")
        with self.assertRaises(Exception):
            check_addr("choucroute")


