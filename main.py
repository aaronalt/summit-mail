import csv
import os
import smtplib
import ssl
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SummitMail:

    today = date.today()

    def __init__(self, sender_email, password, filename, file_source, subject, output="output"):
        self.filename = filename
        self.output = output
        self.file_source = file_source
        self.sender_email = sender_email
        self.password = password
        self.subject = subject
        self.today = date.today()
        self.context = ssl.create_default_context()
        self.message = MIMEMultipart("alternative")
        self.append_list = []
        self.client_list = []

    # Builds email from HTML/text versions in directory
    # file_source is html/text file names
    def build_email(self):
        message = self.message
        message["Subject"] = self.subject
        message["From"] = self.sender_email
        # Open the plain-text and HTML version of your message from external files
        with open(self.file_source + '.txt', 'r') as t:
            text = t.read()
        with open(self.file_source + '.html', 'r') as h:
            html = h.read()
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

    # filter the emails that have already been contacted, returns a list of not contacted emails
    def filter_emails(self):
        with open(self.filename) as file:
            company_list = csv.reader(file)
            for client in company_list:
                company = client[0], client[1], client[2], client[3], client[4], client[5], \
                          client[6], client[7], client[8], client[9], client[10]
                self.client_list.append(company)
            # reads given file and checks if each email has already been contacted

            try:
                with open('email_list.txt', 'r') as e:
                    emails_list = [i.strip('\n') for i in e.readlines()]
                for client in self.client_list:
                    email = client[4]
                    if email in emails_list:
                        print(f"<{email}> already in emails_list")
                    elif email and (email not in emails_list):
                        print(f"added {email}")
                        self.append_list.append(email)
            except FileNotFoundError:
                print("email_list not found!")
            e.close()
        return self.append_list

    # Adds new emails to the list of already contacted emails
    def update_email_list(self):
        with open('email_list.txt', 'a+') as a:
            for i in self.append_list:
                print(i, file=a, sep='\n')
        a.close()
        print("'email_list' appended with new emails...")

    # send the emails once the file has been cleaned
    def send_external(self):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            server.login(self.sender_email, self.password)
            for email in self.append_list:
                server.sendmail(
                    self.sender_email, email, self.message.as_string()
                )
        return "...Done"

    # Use to send to a personal account to test your email
    def send_test_once(self, receiver_email):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, receiver_email, self.message.as_string()
            )
        return "Testing done..."

    # Use this function to test your CSV file
    # First it cleans the file of any missing emails, and counts metrics (number contacted, not contacted, etc.)
    # Then it will write the output to a txt file (output.txt), after deleting the previous version
    # 'test_csv()' will also be called when 'send_external()' runs, cleaning data and providing an output file
    def test_csv(self):
        with open(self.filename) as file:
            company_list = csv.reader(file)

            for client in company_list:
                company = client[0], client[1], client[2], client[3], client[4], client[5], \
                          client[6], client[7], client[8], client[9], client[10]
                self.client_list.append(company)
            # count contacts
            emailed = 0
            empty = 0
            form = 0
            for client in self.client_list:
                if client[4]:
                    emailed += 1
                elif not (client[4]) and (client[6] == 'Contacted'):
                    form += 1
                else:
                    empty += 1
            print(emailed, "...emailed")
            print(empty, '...empty')
            print(form, '...from contact form')

    def write_output(self):
        month = self.today.month
        day = self.today.day
        year = self.today.year
        todays_date = "__" + day + "-" + month + "-" + year
        # write output to a new file
        with open(self.output + todays_date + ".txt", 'wt') as test_file:
            emailed = []
            empty = []
            contact_form = []
            for client in self.client_list:
                if client[4]:
                    emailed.append(client)
                elif not (client[4]) and (client[6] == 'Contacted'):
                    contact_form.append(client)
                else:
                    empty.append(client)
            # write all emailed contacts
            total_emailed = 0
            test_file.write('Emailed:\n----------------------\n')
            for each in emailed:
                total_emailed += 1
                # test_file.write(' - '.join(i for i in each if i))
                test_file.write(f'{each[0]} ({each[2]}) -- {each[1]} -- {each[3]}')
                test_file.write('\n')
            test_file.write('\n\n')
            # write all empty emails
            total_empty = 0
            test_file.write('Not contacted:\n--------------------\n')
            for each in empty:
                total_empty += 1
                test_file.write(f'{each[0]} -- {each[10]}\n')
            # write all contacted from contact form
            total_form = 0
            test_file.write('\n\nContacted from contact form:\n--------------------\n')
            for each in contact_form:
                total_form += 1
                test_file.write(f'{each[0]} ({each[2]}) -- {each[1]} -- {each[3]}')
                test_file.write('\n')
            # write total metrics
            test_file.write('\n--------------------\n')
            test_file.write(f'Total emailed: {total_emailed}\n')
            test_file.write(f'Total not contacted: {total_empty}\n')
            test_file.write(f'Total contacted from form: {total_form}\n')
            test_file.write('--------------------')

    '''     
    # write to new file
    try:
        f = open('email_list.txt', 'r')
        if f:
            os.remove('email_list.txt')
    except FileNotFoundError:
        print("Creating \'email_list.txt\'...")
    email_list = open('email_list.txt', 'wt')
    for each in emailed:
        email_list.write(each[4])
        email_list.write('\n')
    '''


def main():
    # initialize credentials
    test_email = os.getenv('TEST_EMAIL')
    sender = os.getenv('SENDER_EMAIL')
    pw = os.getenv('SENDER_EMAIL_PASSWORD')
    # add new class
    email = SummitMail(sender, pw, "test.csv", "rise", "Summit 2020")
    # build email
    email.build_email()
    # send test email to address specified in env variables
    # email.send_test_once(test_email)
    email.filter_emails()
    # now it will replace 'email_list' - needs to be edited to append to list
    email.update_email_list()
    # email.test_csv()
    # uncomment next line once you are happy with output.txt
    # email.send_external()
    email.write_output()


if __name__ == '__main__':
    main()
