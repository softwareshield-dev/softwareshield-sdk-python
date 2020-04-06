import unittest
import gs

class TestCore(unittest.TestCase):
    def test_getVersion(self):
        self.assertEqual("5.3.8.5 (Release)", gs.Core.getVersion())
    
    """ unittest fitfall: function name can cause test case failure!!!

    def test_init_xxx(self):
        self.assertFalse(gs.init("","",""))
    """
    def test_init_ne2(self):
       # self.assertEqual(gs.Core().LastErrorCode, 0)
        self.assertFalse(gs.Core().init("","",""))
        self.assertTrue(gs.Core().LastErrorCode < 0)

        product_id = "8fb82f54-ecf9-451c-9976-2344aefeaca4"
        path_lic = "Ne2_201908.lic"
        password = "rljycq&3232&RRHP"
        self.assertTrue(gs.Core().init(product_id, path_lic, password))
        self.assertEqual(gs.Core().LastErrorCode, 0)

    def test_getInstance(self):
        core1 = gs.Core.getInstance()
        core2 = gs.Core.getInstance()
        core3 = gs.Core()
        self.assertEqual(core1, core2)
        self.assertEqual(core1, core3)
