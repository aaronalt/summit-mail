from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
import os
from Output import Output
from ClientFilter import ClientFilter


class Email:

    context = ssl.create_default_context()
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_EMAIL_PASSWORD')
    test_email = os.getenv('TEST_EMAIL')

    def __init__(self, subject, html_txt):
        self.subject = subject
        self.message = MIMEMultipart("alternative")
        self.html_txt = html_txt

    def build(self):
        message = self.message
        message["Subject"] = self.subject
        message["From"] = self.sender_email
        with open(self.html_txt + ".txt", "r") as t:
            text = t.read()
        with open(self.html_txt + ".html", "r") as h:
            html = h.read()
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        return message

    def send_test_once(self, send_to):
        message = self.build()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, send_to, message.as_string()
            )
        return "Testing done..."

    def send_external(self, csv_file):
        message = self.build()
        to_filter = ClientFilter(csv_file)
        to_contact = to_filter.filter_emails()
        print("\nClient list to be emailed:\n---------")
        for i in to_contact:
            print(i.name)
        print("-------")
        proceed = input("Proceed? y/n ... ")
        if proceed == 'y':
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
                server.login(self.sender_email, self.password)
                for email in to_contact:
                    server.sendmail(
                        self.sender_email, email, message.as_string()
                    )
            print("\n")
        else:
            print("Aborting the mission...")
