import unittest
import gs

class TestGS5(unittest.TestCase):
    def test_getVersion(self):
        self.assertEqual("5.3.8.5 (Release)", gs.getVersion())


