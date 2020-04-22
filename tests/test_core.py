import unittest
import gs
import os
from datetime import datetime, timedelta

def getPathToTestCaseLicense(prj):
    return os.path.join(os.getcwd(), "tests", "data", prj)

test_project = {
    "buildId": 32,
    "productId": "8fb82f54-ecf9-451c-9976-2344aefeaca4",
    "productName": "Ne2_201908",
    "pathLic": getPathToTestCaseLicense("Ne2_201908_b32.lic"),
    "password": "rljycq&3232&RRHP"
}


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

def init_core(self):
    core = gs.Core()
    #self.assertFalse(core.init("","",""))
    #self.assertTrue(core.LastErrorCode < 0)

    self.assertTrue(core.init(test_project['productId'], test_project['pathLic'], test_project['password']))
    self.assertEqual(core.lastErrorCode, 0)



class TestCoreAPI(unittest.TestCase):
#    def test_init_m(self):
#        self.assertFalse(gs.Core().init("","",""))
    def setUp(self):
        init_core(self)

    @classmethod
    def tearDownClass(cls):
        gs.Core().cleanUp()

    def test_productInfo(self):
        '''product info'''
        self.assertEqual(gs.Core().productId, test_project['productId'])
        self.assertEqual(gs.Core().productName, test_project['productName'])
        self.assertEqual(gs.Core().buildId, test_project['buildId'])
    
    def test_entity(self):
        entities = gs.Core().entities
        self.assertEqual(len(entities), 1)

        eid0 = "62a6ec4c-c05a-4fae-be40-2011a79f8c62"
        e0 = entities[0]
        self.assertEqual(e0.id, eid0)
        self.assertEqual(e0.name, "E1")

        at = e0.attribute
        print(at)

        self.assertEqual(e0, gs.Core().getEntityById(eid0))

        with self.assertRaises(gs.SdkError):
            gs.Core().getEntityById("x1")
        
        # not being accessed
        self.assertFalse(e0.accessing)
        self.assertTrue(e0.autoStart)

        self.assertEqual(e0.accessible, e0.license.valid)
        self.assertEqual(e0.locked, e0.license.locked)
        self.assertEqual(e0.unlocked, e0.license.unlocked)

        if e0.accessible:
            self.assertTrue(e0.beginAccess())
            self.assertTrue(e0.accessing)
            self.assertTrue(e0.endAccess())
        else:
            self.assertTrue(e0.locked)
            self.assertFalse(e0.unlocked)

    def test_var(self):
        ''' test variable '''
        core = gs.Core()
        with self.assertRaises(gs.SdkError):
            core.getVariable("level")

        age = core.getVariable("age")
        self.assertEqual(age.name, "age")
        self.assertEqual(age.value, 10)

        nm = core.getVariable("name")
        self.assertEqual(nm.name, "name")
        self.assertEqual(nm.value, "randy")

        self.assertEqual(core.getVariable("male").value, True)
        self.assertEqual(core.getVariable("salary").value, 123.5)

        t = core.getVariable("birthday").value
        self.assertEqual(str(t), '2020-04-01 22:00:00')

        # set
        def writeTest(vname, v):
            x = core.getVariable(vname)
            old_v = x.value
            x.value = v
            if isinstance(v, float):
                self.assertAlmostEqual(x.value,v, delta=0.1)
            else:
                self.assertEqual(x.value, v)
            x.value = old_v

        writeTest("age", 123)
        writeTest("name", "janet")
        writeTest("male", False)
        writeTest("salary", 888.88)
        dt = datetime.fromtimestamp(int(datetime.now().timestamp()))
        writeTest("birthday", dt)

    def test_licenseParam(self):
        lic = gs.Core().entities[0].license
        print("lic: %s" % lic.name)
        print(lic.params)

        isp = lic.inspector
        print("ISP: %r" % isp)

    def test_action0(self):
        req = gs.Core().createRequest()
        act = req.addAction(gs.ActionId.ACT_UNLOCK)
        self.assertEqual(act.id, gs.ActionId.ACT_UNLOCK)
        with self.assertRaises(gs.SdkError):
            req.addAction(gs.ActionId.ACT_ADD_ACCESSTIME, gs.Core().entities[0])
            
        print(req.code)


    def test_action1(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        for actId in gs.ActionId:
            act = req.addAction(actId)
            print(act, '\n')
            self.assertEqual(act.id, actId)
            
        print('\n', '*'*30)


    def test_action_clean(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        act = req.addAction(gs.ActionId.ACT_CLEAN)
        self.assertFalse(act.hasExpireDate)

        act.expireDate = datetime.now() + timedelta(days = 10)
        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)

    def test_action_addAccessTime(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        
        act = req.addAction(gs.ActionId.ACT_ADD_ACCESSTIME)
        act.addedTimes = 10

        self.assertEqual(act.addedTimes, 10)

        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)

    def test_action_setAccessTime(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        
        act = req.addAction(gs.ActionId.ACT_SET_ACCESSTIME)
        act.times = 10

        self.assertEqual(act.times, 10)

        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)


    def test_action_setStartDate(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        
        act = req.addAction(gs.ActionId.ACT_SET_STARTDATE)
        self.assertFalse(act.hasStartDate)

        dt = datetime(2020, 6,1)
        act.startDate = dt
        self.assertEqual(act.startDate, dt)

        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)


    def test_action_setEndDate(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        
        act = req.addAction(gs.ActionId.ACT_SET_ENDDATE)
        self.assertFalse(act.hasEndDate)

        dt = datetime(2021, 6,1)
        act.endDate = dt
        self.assertEqual(act.endDate, dt)

        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)

    def test_action_setSessionTime(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        
        act = req.addAction(gs.ActionId.ACT_SET_SESSIONTIME)
        act.sessionTime = 100
        self.assertEqual(act.sessionTime, 100)

        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)

    def test_action_setPeriod(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        
        act = req.addAction(gs.ActionId.ACT_SET_EXPIRE_PERIOD)
        act.period = 1000
        self.assertEqual(act.period, 1000)

        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)

    def test_action_addPeriod(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        
        act = req.addAction(gs.ActionId.ACT_ADD_EXPIRE_PERIOD)
        act.addedPeriod = 200
        self.assertEqual(act.addedPeriod, 200)

        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)

    def test_action_setDuration(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        
        act = req.addAction(gs.ActionId.ACT_SET_EXPIRE_DURATION)
        act.duration = 1000
        self.assertEqual(act.duration, 1000)

        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)

    def test_action_addDuration(self):
        req = gs.Core().createRequest()
        print('\n', '*'*30)
        
        act = req.addAction(gs.ActionId.ACT_ADD_EXPIRE_DURATION)
        act.addedDuration = 250
        self.assertEqual(act.addedDuration, 250)

        print(act, '\n')
        print(f"code={req.code}")
            
        print('\n', '*'*30)


    def test_online_activation(self):
        core = gs.Core()
        
        if core.isServerAlive():
            print("license server is online")

            sn = 'xxx-yyy-zzz'
            self.assertFalse(core.isValidSN(sn))

            self.assertTrue(core.isValidSN('0875-BB91-4449-9DCE'))

            self.assertTrue(core.applySN('0BD3-4F5C-4EB4-9EE9'))

            self.assertTrue(core.revokeSN('0BD3-4F5C-4EB4-9EE9'))

            self.assertTrue(core.isAllEntitiesLocked())

        else:
            print("license server is offline")

    def test_offline_activation(self):
        core = gs.Core()
        code = 'TUVP-C9NM-PRRO-GH33-5KC3'
        sn = '0BD3-4F5C-4EB4-9EE9'
        self.assertTrue(core.applyLicenseCode(code, sn))

    def test_unlock(self):
        core = gs.Core()
        code = core.entities[0].license.unlockRequestCode
        print(f"e0.lic.unlockReqCode: {code}")
        print(f"core.unlockReqCode: {core.unlockRequestCode}")
        print(f"core.cleanReqCode: {core.cleanRequestCode}")
        print(f"core.fixReqCode: {core.fixRequestCode}")

    def test_allEntityStatus(self):
        """ clean action must be applied before this test starts! """
        print("\n\nplease make sure clean the license before testing!\n")
        core = gs.Core()

        self.assertFalse(core.isAllEntitiesLocked())
        self.assertFalse(core.isAllEntitiesUnlocked())

        # lock it!
        print("Lock it...\n")
        core.lockAllEntities()
        self.assertTrue(core.isAllEntitiesLocked())

        print("Unlock it...\n")
        code = 'TUVP-C9NM-PRRO-GH33-5KC3'
        sn = '0BD3-4F5C-4EB4-9EE9'
        self.assertTrue(core.applyLicenseCode(code, sn))
        self.assertTrue(core.isAllEntitiesUnlocked())


class TestEvents(unittest.TestCase):
    def test_app_monitor(self):
        pass
    def test_entity_monitor(self):
        init_core(self)
        
        e0 = gs.Core().entities[0]

        @gs.entity_access_heartbeat
        def ping(entity, event):
            print("ping >>")

        @gs.entity_access_started
        def onStarted(entity, event):
            print("started >>")

        @gs.entity_access_starting
        @gs.entity_access_started
        def handler(e: gs.Entity, event):
            print(f"entity {e.name} on {event} >>")
            self.assertEqual(e.id, e0.id)

        e0.beginAccess()

        import time

        print("sleep for 60 seconds...")
        time.sleep(10)

        e0.endAccess()



    def test_license_monitor(self):
        self.loading_called = False
        @gs.license_loading
        def loading(_):
            print("\nlicense loading...")
            self.loading_called = True

        self.loaded_called = False
        @gs.license_loaded
        def loaded(_):
            print("done!\n")
            self.loaded_called = True

        self.virgin_called = False
        @gs.license_new_install
        def newinstall(_):
            print("new install...")
            self.virgin_called = True

        self.fail_called = False
        @gs.license_fail
        def bad(_):
            print("BAD!\n")
            self.fail_called = True

        init_core(self)

        self.assertTrue(self.loading_called)
        self.assertTrue(self.loaded_called or self.fail_called)
        self.assertFalse(self.virgin_called)