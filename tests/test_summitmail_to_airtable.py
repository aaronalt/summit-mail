from __future__ import absolute_import

import unittest

from actions.summitmail_to_airtable import SummitMail
from actions.util import cfg_from_selection, run
from gui.creds import Creds


class SummitMailToAirtableTest(unittest.TestCase):

    def setUp(self):
        # todo: learn config file name from ENV variables
        # self.cfg_input = input("config file name: ")
        # config = f'{self.cfg_input}.ini'
        self.config = 'new contacts'
        cfg_from_selection(f'{self.config}.ini')
        self.table_name = "test_table"
        self.summitmail = SummitMail(Creds.base_id, table_name=self.table_name)
        # delete all records from test table
        self.all_contacts = self.summitmail.get_all_contacts()
        for each in self.all_contacts:
            try:
                self.summitmail.delete_contact(each['fields']['name'])
            except KeyError:
                self.summitmail.delete_contact("blank", record_id=each['id'])
        # add new test records
        self.new_test_records = [
            {
                "id": "rec036oHPuD0EtNhP",
                "fields": {
                    "name": "synergy",
                    "country": "India",
                    "website": "http://synergy.co/",
                    "email": "hell@0synergy.co",
                    "status": "Contacted",
                    "contact date": "2020-05-27",
                    "result": "No response",
                    "source": "online"
                },
                "createdTime": "2020-05-27T07:44:56.000Z"
            },
            {
                "id": "reccdjhXaxdIejw1t",
                "fields": {
                    "name": "coffee",
                    "country": "Ukraine",
                    "website": "https://coffee.co/",
                    "email": "m@coffee.com",
                    "status": "Contacted",
                    "contact date": "2020-05-27",
                    "result": "No response",
                    "source": "referral"
                },
                "createdTime": "2020-05-27T07:26:13.000Z"
            },
            {
                "id": "recWH7wg7kDKBi0yt",
                "fields": {
                    "name": "logics",
                    "country": "United States",
                    "website": "http://logics.io/",
                    "email": "info@logics.io",
                    "status": "Contacted",
                    "contact date": "2020-06-18",
                    "result": "No response",
                    "contact method": "Email",
                    "source": "conference"
                },
                "createdTime": "2020-06-18T14:09:01.000Z"
            }
        ]

    def test_cfg_from_selection(self):
        self.assertEqual(self.config, Creds.cfg_name)
        self.assertTrue(Creds.api_key)
        self.assertTrue(Creds.base_id)

    def test_filter_contacts(self):
        contact_list = self.summitmail.filter_contacts(self.new_test_records)
        self.assertTrue(contact_list)
        self.assertEqual(len(contact_list), len(self.new_test_records))



    def tearDown(self):
        for each in self.all_contacts:
            try:
                self.summitmail.delete_contact(each['fields']['name'])
            except KeyError:
                self.summitmail.delete_contact("blank", each['id'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
