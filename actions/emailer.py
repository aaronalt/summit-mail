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

    def __init__(self, subject, files_source, file_path='../docs/inputs/'):
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
        self.send_to = ""
        self.rec_list = []

    def build_and_send(self, to_addrs=None, host="smtp.gmail.com", port=465, write_output=True,
                      output_path="../docs/outputs/"):
        # build
        if to_addrs is None:
            to_addrs = self.test_email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = self.subject
        msg["From"] = self.sender_email
        msg["To"] = to_addrs
        msg["Bcc"] = ""
        try:
            with open(self.files_source_txt, "r") as t:
                text = t.read()
            with open(self.files_source_html, "r") as h:
                html = h.read()
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            msg.attach(part1)
            msg.attach(part2)

            # send
            with smtplib.SMTP_SSL(host, port, context=self.context) as server:
                server.login(self.sender_email, self.password)
                try:
                    server.sendmail(
                        self.sender_email, to_addrs, msg.as_string()
                    )
                    print(f"email sent to {to_addrs}")
                except smtplib.SMTPRecipientsRefused as e:
                    dialog_error(Dialog(), "SMTP Error", f"Couldn't send email to:\ne",
                                 traceback.format_exc())
                    print(f"email \'{to_addrs}\' not found")
        except FileNotFoundError:
            return ""

    def filter_list(self, client_list, write_output=False, output_path="../docs/outputs/"):
        for each in client_list:
            self.rec_list.append(each)
            self.build_and_send(each.email)
        if write_output:
            output = Output(self.rec_list, output_path)
            filepath = output.write()
            return filepath

    def build_message(self, to_addrs=None):
        if to_addrs is None:
            to_addrs = self.send_to
        message = self.message
        message["Subject"] = self.subject
        message["From"] = self.sender_email
        message["To"] = ', '.join(to_addrs)
        message["Bcc"] = ""
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

    def send_test_once(self, to_addrs=None, sender=None, host="smtp.gmail.com", port=465, server_host=None,
                       server_pw=None):
        if sender is None:
            sender = self.sender_email
        if server_host is None:
            server_host = self.sender_email
        if server_pw is None:
            server_pw = self.password
        if to_addrs is None:
            to_addrs = self.test_email

        with smtplib.SMTP_SSL(host, port) as server:
            try:
                message = self.build_message(to_addrs)
                server.login(server_host, server_pw)
                server.send_message(
                    message, sender, to_addrs
                )
            except smtplib.SMTPAuthenticationError:
                return traceback.format_exc()
        return 0

    def send_external(self, clients_list, host="smtp.gmail.com", port=465, write_output=True,
                      output_path="../docs/outputs/"):
        output = Output(clients_list, output_path)
        #message = self.build_message()
        filepath = Path()
        if write_output:
            filepath = output.write()
        for each in clients_list:
            self.rec_list.append(each.email)
        with smtplib.SMTP_SSL(host, port, context=self.context) as server:
            server.login(self.sender_email, self.password)

            try:
                message = self.build_message(self.rec_list)
                server.sendmail(
                    self.sender_email, self.rec_list, message.as_string()
                )
            except smtplib.SMTPRecipientsRefused as e:
                dialog_error(Dialog(), "SMTP Error", f"Couldn't send email to:\ne",
                             traceback.format_exc())
                pass
        return filepath
