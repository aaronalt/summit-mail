from __future__ import absolute_import
import unittest

from items.client import Client


class SummitmailToAirtableTest(unittest.TestCase):

    def setUp(self):
        contacts = []
        contact_1 = Client("Microsoft", "USA", "microsoft.com", "test@microrgsoft.com")
        contact_2 = Client("Apple", "USA", "apple.org", "info@arpple.com")
        contact_3 = Client("JetBrains", "Czechia", "jetbrains.com", "info@jertbrains.com")
        contacts.append(contact_1)
        contacts.append(contact_2)
        contacts.append(contact_3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
