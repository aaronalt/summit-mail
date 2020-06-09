import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
import os
from Output import Output
from ClientFilter import ClientFilter


class Email:

    def __init__(self, subject, html_txt, cfg_name):
        self.subject = subject
        self.html_txt = f'{html_txt}.txt'

        self.cfg_name = cfg_name
        self.cfg = configparser.ConfigParser()
        self.cfg.read(os.path.join('Cfg/', self.cfg_name))
        self.sender_email = self.cfg['settings']['sender_email']
        self.password = self.cfg['settings']['sender_email_password']
        self.test_email = self.cfg['settings']['test_email']

        # build message
        self.context = ssl.create_default_context()
        self.message = MIMEMultipart("alternative")
        message = self.message
        message["Subject"] = self.subject
        message["From"] = self.sender_email
        with open(self.html_txt, "r") as t:
            text = t.read()
        with open(self.html_txt, "r") as h:
            html = h.read()
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

    def send_test_once(self, send_to):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, send_to, self.message.as_string()
            )
        return "Testing done..."

    def send_external(self, clients_list, write_output=True):
        # to_filter = ClientFilter(csv_file)
        # to_contact = to_filter.filter_emails()
        output = Output(clients_list)
        if write_output:
            output.write()
        proceed = input("Proceed  with emailing? y/n ... ")
        if proceed == 'y':
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
                server.login(self.sender_email, self.password)
                for each in clients_list:
                    try:
                        server.sendmail(
                            self.sender_email, each.email, self.message.as_string()
                        )
                    except smtplib.SMTPRecipientsRefused as e:
                        print(e)
                        clients_list.pop(each)
                        pass
            print("\n")
        else:
            print("Aborting the mission...")
