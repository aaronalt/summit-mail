from __future__ import absolute_import

import os
from smtplib import SMTPAuthenticationError
import unittest
from pathlib import Path

from actions.emailer import Email
from gui.creds import Creds
from actions.util import cfg_from_selection
import configparser

from items.client import Client


class EmailerTest(unittest.TestCase):

    def setUp(self):
        self.subject = 'Re: Test Email'
        self.files_source = 'test'
        self.filepath = '../docs/test_docs'
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
        cfg_from_selection(f'{self.creds.cfg_name}.ini')
        self.email = Email(self.subject, self.files_source, self.filepath)

        self.clients_list = [Client("test1", "testland", "t.com", "test1@t.com"),
                             Client("test2", "testland", "e.com", "test2@t.com"),
                             Client("test3", "testland", "r-74.co", "test3@t.com"),
                             Client("test4", "testland", "p.me", "test4@t.com"),
                             Client("test5", "testland", "rrr.io", "test5@t.com")]

    def test_build_message(self):
        message = self.email.build_message()
        self.assertEqual(message['Subject'], self.subject)
        self.assertEqual(message['From'], self.creds.sender_email)
        email_blank = Email(self.subject, "")
        self.assertFalse(email_blank.build_message())

    def test_send_test_once(self):
        no_creds = self.email.send_test_once()
        self.assertTrue(no_creds)
        # todo: test with actual working credentials

    def test_send_external(self):
        # no_creds = self.email.send_external(self.clients_list,
        #                         output_path="../docs/test_docs/")
        self.assertRaises(SMTPAuthenticationError)

    def tearDown(self):
        for root, dirs, files in os.walk("../config"):
            for file in files:
                if file.startswith('test'):
                    path = Path(root) / file
                    os.remove(path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
