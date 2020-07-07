from __future__ import absolute_import
import unittest
from gui.creds import Creds


class CredsTest(unittest.TestCase):

    def setUp(self):
        self.baseid = "id000000"
        self.apikey = "key00000"
        self.cfgname = "CfgName"
        self.senderemail = "sender@email.com"
        self.pw = "sdo$Kf9j"
        self.testemail = "test@email.com"
        self.test_creds = Creds(self.baseid,
                                self.apikey,
                                self.cfgname,
                                self.senderemail,
                                self.pw,
                                self.testemail)

    def test_init_of_creds_success(self):
        self.assertEqual(self.test_creds.base_id, self.baseid)
        self.assertTrue(hasattr(self.test_creds, "base_id"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
