import unittest
from main import SummitMail
import os


class BuildEmailTest(unittest.TestCase):
    def setUp(self):
        sender = os.getenv('SENDER_EMAIL')
        pw = os.getenv('SENDER_EMAIL_PASSWORD')
        self.email = SummitMail(sender, pw, "test.csv", "rise", "Summit 2020")

    def test_subject(self):
        self.assertTrue(self.email.subject)


if __name__ == '__main__':
    unittest.main()
