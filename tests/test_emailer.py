from __future__ import absolute_import

import os
import unittest
from pathlib import Path

from summitemailer.actions import util
from summitemailer.actions import emailer
from summitemailer.gui import creds
from summitemailer.actions.util import cfg_from_selection
import configparser

from summitemailer.items.client import Client


class EmailerTest(unittest.TestCase):

    def setUp(self):
        self.subject = 'Re: Test Email'
        self.files_source = 'test'
        self.filepath = f'/docs/test_docs'
        # using Mailtrap.io creds
        self.creds = creds.Creds('id', 'apikey', 'test_config', 'aaron@mango-byte.com', 'tchxhfugdhlxaokx',
                           'aaronalt07@gmail.com')
        cfg = configparser.ConfigParser()
        cfg['ENV'] = {'cfg_name': str(self.creds.cfg_name),
                      'airtable_api_key': str(self.creds.api_key),
                      'airtable_base_id': str(self.creds.base_id)}
        cfg['settings'] = {'sender_email': str(self.creds.sender_email),
                           'sender_email_password': str(self.creds.sender_email_pw),
                           'test_email': str(self.creds.test_email)}
        with open(f'{util.resource_path()}/config/{self.creds.cfg_name}.ini', 'w') as configfile:
            cfg.write(configfile)
        cfg_from_selection(f'{self.creds.cfg_name}.ini')
        self.email = emailer.Email(self.subject, self.files_source, self.filepath)

        self.clients_list = [Client("test1", "testland", "t.com", "aaronalt07@gmail.com"),
                             Client("test2", "testland", "e.com", "aaronalt08@gmail.com"),
                             Client("test3", "testland", "r-74.co", "aaronalt09@gmail.com"),
                             Client("test4", "testland", "p.me", "aaronalt06@gmail.com"),
                             Client("test5", "testland", "rrr.io", "aaronalt05@gmail.com")]


    def test_connection(self):
        message = self.email.build_and_send(conn_test=True)
        self.assertTrue(message)

    def test_send_test_once(self):
        # no_creds = self.email.send_test_once("aaron@mango-byte.com")
        # self.assertFalse(no_creds)
        new_func = self.email.build_and_send("aaronalt08@gmail.com")
        self.assertFalse(new_func)


    def test_send_external(self):
        # emails_sent = self.email.send_external(self.clients_list, write_output=True,
                                               #output_path="../docs/test_docs/output")
        # self.assertTrue(emails_sent)
        send_tolist = self.email.filter_list(self.clients_list, write_output=False,
                                             output_path=f"{util.resource_path()}/docs/test_docs/outputs")
        self.assertTrue(send_tolist)

    def tearDown(self):
        for root, dirs, files in os.walk(f"{util.resource_path()}/config"):
            for file in files:
                if file.startswith('test'):
                    path = Path(root) / file
                    os.remove(path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
