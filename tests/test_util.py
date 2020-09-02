from __future__ import absolute_import

import configparser
import unittest

from actions.summitmail_to_airtable import SummitMail
from actions.util import cfg_from_selection
from gui.creds import Creds


class UtilTest(unittest.TestCase):

    def setUp(self):
        self.cfg_input = input("config file name: ")
        config = f'{self.cfg_input}.ini'
        # cfg = configparser.ConfigParser()
        cfg_from_selection(config)

    def test_cfg_from_selection(self):
        self.assertEqual(self.cfg_input, Creds.cfg_name)
        self.assertTrue(Creds.api_key)
        self.assertTrue(Creds.base_id)

    def test_run(self):
        summitmail = SummitMail()



if __name__ == '__main__':
    unittest.main(verbosity=2)
