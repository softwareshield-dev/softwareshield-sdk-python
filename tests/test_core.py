import unittest
import gs

class TestCore(unittest.TestCase):
    def test_getVersion(self):
        self.assertEqual("5.3.8.5 (Release)", gs.getVersion())

    def test_init(self):
        self.assertFalse(gs.init("","",""))


