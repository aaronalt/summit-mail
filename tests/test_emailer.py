from __future__ import absolute_import
import unittest
from actions.emailer import Email
from gui.creds import Creds
from actions.util import cfg_from_selection
import configparser


class EmailerTest(unittest.TestCase):

    def setUp(self):
        self.subject = 'Re: Test Email'
        self.files_source = 'test'
        self.filepath = '../docs/test_docs'
        self.email = Email(self.subject, self.files_source, self.filepath)
        self.creds = Creds('id', 'apikey', 'test_config', 'aaron@mango-byte.com', 'pw', 'aaronalt07@gmail.com')

        cfg = configparser.ConfigParser()
        cfg['ENV'] = {'cfg_name': str(self.creds.cfg_name),
                      'airtable_api_key': str(self.creds.api_key),
                      'airtable_base_id': str(self.creds.base_id)}
        cfg['settings'] = {'sender_email': str(self.creds.sender_email),
                           'sender_email_password': str(self.creds.sender_email_pw),
                           'test_email': str(self.creds.test_email)}
        with open(f'../config/{self.creds.cfg_name}.ini', 'w') as configfile:
            cfg.write(configfile)

    def test_build_message(self):
        message = self.email.build_message()
        self.assertEqual(message['Subject'], self.subject)
        self.assertEqual(message['From'], self.creds.sender_email)
        cfg_from_selection()


if __name__ == '__main__':
    unittest.main(verbosity=2)
