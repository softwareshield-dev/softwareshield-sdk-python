import unittest
import gs
import os


def getPathToTestCaseLicense(prj):
    return os.path.join(os.getcwd(), "tests", "data", prj)

class TestCoreStatic(unittest.TestCase):
    ''' Test static members of gs.Core '''
    def test_getVersion(self):
        '''sdk version'''
        self.assertEqual("5.3.8.5 (Release)", gs.Core.getVersion())

    def test_getInstance(self):
        ''' singleton api '''
        core1 = gs.Core.getInstance()
        core2 = gs.Core.getInstance()
        core3 = gs.Core()
        self.assertEqual(core1, core2)
        self.assertEqual(core1, core3)

        # if core not initialized, LastErrorCode is not available
        with self.assertRaises(Exception):
            i = core3.lastErrorCode
            print("i=%d", i)

class TestCoreAPI(unittest.TestCase):
#    def test_init_m(self):
#        self.assertFalse(gs.Core().init("","",""))
    def setUp(self):
        core = gs.Core()
        #self.assertFalse(core.init("","",""))
        #self.assertTrue(core.LastErrorCode < 0)

        self.buildId = 31
        self.productId = "8fb82f54-ecf9-451c-9976-2344aefeaca4"
        self.productName = "Ne2_201908"
        self.pathLic = getPathToTestCaseLicense("Ne2_201908.lic")
        self.password = "rljycq&3232&RRHP"

        self.assertTrue(core.init(self.productId, self.pathLic, self.password))
        self.assertEqual(core.lastErrorCode, 0)

    @classmethod
    def tearDownClass(cls):
        gs.Core().cleanUp()

    def test_productInfo(self):
        '''product info'''
        self.assertEqual(gs.Core().productId, self.productId)
        self.assertEqual(gs.Core().productName, self.productName)
        self.assertEqual(gs.Core().buildId, self.buildId)


