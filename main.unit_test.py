import unittest
from main import SummitMail
import os


class EmailTest(unittest.TestCase):
    def setUp(self):
        sender = os.getenv('SENDER_EMAIL')
        pw = os.getenv('SENDER_EMAIL_PASSWORD')
        self.email = SummitMail(sender, pw, "test.csv", "test", "Summit 2020")

    def test_build_email(self):
        self.email.build_email()
        self.assertTrue(self.email.message)
        self.assertTrue(self.email.subject)
        self.assertTrue(self.email.subject == "Summit 2020")
        self.assertFalse(self.email.sender_email)
        self.assertTrue(os.path.exists('rise.txt'))
        self.assertTrue(os.path.exists('rise.html'))

    def test_filter_emails(self):
        with open('test.csv', 'a') as csv:
            line = "Test Company 100,category,country,website.com,test@website.com,,,,,,,"
            csv.write(line)
        self.email.filter_emails("email_list_test")
        self.assertTrue(self.email.client_list)
        # delete appended line of file
        with open('test.csv', 'r') as csv:
            lines = csv.readlines()[:-1]
        os.remove('test.csv')
        self.assertFalse((os.path.exists('test.csv')))
        with open('test.csv', 'wb') as csv:
            for line in lines:
                csv.write(line)
        self.assertTrue((os.path.exists('test.csv')))

    def test_update_email_list(self):
        self.test_filter_emails()
        self.assertTrue(self.email.append_list)
        with open('email_list_test.txt', 'r') as email_list:
            line = email_list.readlines()
            liszt = [i.strip() for i in line]
            self.assertFalse(self.email.append_list in liszt)
        self.email.update_email_list()
        with open('email_list_test.txt', 'r') as email_list:
            line = email_list.readlines()[:-1]
            print(line)
        os.remove('email_list_test.txt')
        with open('email_list_test.txt', 'w') as new_email_list:
            for i in line:
                new_email_list.write(i)

    #def test_write_output(self):


if __name__ == '__main__':
    unittest.main()
