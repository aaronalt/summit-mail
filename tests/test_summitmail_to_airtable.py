from __future__ import absolute_import
import unittest

from actions.summitmail_to_airtable import SummitMail


class SummitmailToAirtableTest(unittest.TestCase):

    def setUp(self):
        self.contacts = [
            {
                "id": "rec036oHPuD0EtNhJ",
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
                "id": "reccdjhXaxdIejw1q",
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
                "id": "recWH7wg7kDKBi0yq",
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

    def test_filter_contacts(self):
        filtered = SummitMail()
        self.assertRaises(TypeError, filtered)
        test_contacts = SummitMail("Test", self.contacts)
        test_contacts_filtered = test_contacts.filter_contacts(self.contacts)
        self.assertTrue(test_contacts_filtered)
        self.assertEqual(len(test_contacts_filtered), len(self.contacts))


if __name__ == '__main__':
    unittest.main(verbosity=2)
