import unittest
from main import SummitMail
import os


class EmailTest(unittest.TestCase):
    def setUp(self):
        sender = os.getenv('SENDER_EMAIL')
        pw = os.getenv('SENDER_EMAIL_PASSWORD')
        self.email = SummitMail(sender, pw, "test.csv", "rise", "Summit 2020")

    def test_build_email(self):
        self.email.build_email()
        self.assertTrue(self.email.message)
        self.assertTrue(self.email.subject)
        self.assertTrue(self.email.subject == "Summit 2020")
        self.assertFalse(self.email.sender_email)
        self.assertTrue(os.path.exists('rise.txt'))
        self.assertTrue(os.path.exists('rise.html'))


if __name__ == '__main__':
    unittest.main()
