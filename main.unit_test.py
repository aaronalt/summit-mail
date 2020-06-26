import unittest
from main import SummitMail
import os
from datetime import date


class EmailTest(unittest.TestCase):

    today = date.today()

    def setUp(self):
        sender = os.getenv('SENDER_EMAIL')
        pw = os.getenv('SENDER_EMAIL_PASSWORD')
        self.email = SummitMail(sender, pw, "Outputs/Tests/test.csv", "Outputs/Tests/test", "Summit 2020")

    def test_build_email(self):
        self.email.build_email()
        self.assertTrue(self.email.message)
        self.assertTrue(self.email.subject)
        self.assertTrue(self.email.subject == "Summit 2020")
        self.assertFalse(self.email.sender_email)

    def test_filter_emails(self):
        with open('Inputs/Tests/test.csv', 'a') as csv:
            line = "Test Company 100,category,country,website.com,test@website.com,,,,,,,"
            csv.write(line)
        self.email.filter_emails("Outputs/Tests/email_list_test")
        self.assertTrue(self.email.client_list)
        # delete appended line of file
        with open('Inputs/Tests/test.csv', 'r') as csv:
            lines = csv.readlines()[:-1]
        os.remove('Inputs/Tests/test.csv')
        self.assertFalse((os.path.exists('Inputs/Tests/test.csv')))
        with open('Inputs/Tests/test.csv', 'wb') as csv:
            for line in lines:
                csv.write(line)
        self.assertTrue((os.path.exists('Inputs/Tests/test.csv')))

    def test_update_email_list(self):
        self.test_filter_emails()
        self.assertTrue(self.email.append_list)
        with open('docs/test_docs/email_list_test.txt', 'r') as email_list:
            line = email_list.readlines()
            liszt = [i.strip() for i in line]
            self.assertFalse(self.email.append_list in liszt)
        self.email.update_email_list("Outputs/Tests/email_list_test")
        with open('docs/test_docs/email_list_test.txt', 'r') as email_list:
            line = email_list.readlines()[:-1]
            print(line)
        os.remove('docs/test_docs/email_list_test.txt')
        with open('docs/test_docs/email_list_test.txt', 'w') as new_email_list:
            for i in line:
                new_email_list.write(i)

    def test_sub_directory(self):
        self.assertTrue(os.path.exists('Inputs/Tests/test.csv'))
        self.assertTrue(os.path.exists('Inputs/Tests/test.txt'))
        self.assertTrue(os.path.exists('Inputs/Tests/test.html'))
        self.assertTrue(os.path.exists('docs/test_docs/email_list_test.txt'))

    def test_write_output(self):
        month = self.today.month
        day = self.today.day
        year = self.today.year
        date_today = "__" + str(day) + "_" + str(month) + "_" + str(year)
        self.email.write_output("Outputs/Tests/", "output_test")
        self.assertTrue(os.path.exists("Outputs/Tests/output_test" + date_today + ".txt"))


if __name__ == '__main__':
    unittest.main()
