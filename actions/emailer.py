import configparser
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from pathlib import Path

from actions.output import Output
from gui import dialog_error
from gui.creds import Creds
from gui.dialog import Dialog


class Email:

    def __init__(self, subject, files_source, file_path='../docs'):
        self.context = ssl.create_default_context()
        self.message = MIMEMultipart("alternative")
        self.subject = subject
        self.files_source_txt = f'{file_path}/{files_source}.txt'
        self.files_source_html = f'{file_path}/{files_source}.html'
        self.cfg_name = f"../config/{Creds.cfg_name}.ini"
        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.cfg_name)
        self.sender_email = self.cfg['settings']['sender_email']
        self.password = self.cfg['settings']['sender_email_password']
        self.test_email = self.cfg['settings']['test_email']

    def build_message(self):
        message = self.message
        message["Subject"] = self.subject
        message["From"] = self.sender_email
        try:
            with open(self.files_source_txt, "r") as t:
                text = t.read()
            with open(self.files_source_html, "r") as h:
                html = h.read()
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            return message
        except FileNotFoundError:
            return ""

    def send_test_once(self):
        message = self.build_message()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            try:
                server.login(self.sender_email, self.password)
                server.sendmail(
                    self.sender_email, self.test_email, message.as_string()
                )
            except smtplib.SMTPAuthenticationError:
                return traceback.format_exc()
        return 0

    def send_external(self, clients_list, write_output=True, output_path="../docs/outputs/"):
        message = self.build_message()
        output = Output(clients_list, output_path)
        filepath = Path()
        if write_output:
            filepath = output.write()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            server.login(self.sender_email, self.password)
            for each in clients_list:
                try:
                    server.sendmail(
                        self.sender_email, each.email, message.as_string()
                    )
                except smtplib.SMTPRecipientsRefused as e:
                    dialog_error(Dialog(), "SMTP Error", f"Couldn't send email to {each.email}:\ne",
                                 traceback.format_exc())
                    pass
        return filepath
