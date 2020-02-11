import unittest
from main import SummitMail
import os


class EmailTest(unittest.TestCase):
    def setUp(self):
        sender = os.getenv('SENDER_EMAIL')
        pw = os.getenv('SENDER_EMAIL_PASSWORD')
        '''        
        # create fake csv
        self.fake_csv = tempfile.TemporaryFile('w+b')
        with self.fake_csv as csv:
            print("Creating fake csv...")
            headers = ['name', 'category', 'country', 'website', 'email', 'stage', 'status', 'contact date',
                       'contact method', 'result', 'error result', 'note']
            header_line = ','.join(i for i in headers)
            csv.write(header_line + "\n")
            tester = ['John Smith', 'Security', 'U.S.A', 'www.johnsmith.com', 'johnsmith@test.com', 'Alpha', '', '', '',
                      '', '', '', '']
            tester_line = ','.join(i for i in tester)
            csv.write(tester_line)
            print("...done.")
            csv.seek(0)
            print("Temp file:")
            print(csv.read())
            '''
        self.email = SummitMail(sender, pw, "test.csv", "rise", "Summit 2020")

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
        self.email.filter_emails()
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
    # def tearDown(self):
        # self.fake_csv.close()


if __name__ == '__main__':
    unittest.main()
