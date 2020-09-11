import configparser
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from pathlib import Path

from summitemailer.actions import output
from summitemailer.actions import util
from summitemailer.gui import dialog_error
from summitemailer.gui import creds
from summitemailer.gui.dialog import Dialog


class Email:

    def __init__(self, subject, files_source, file_path='/docs/inputs/'):
        self.context = ssl.create_default_context()
        self.message = MIMEMultipart("alternative")
        self.subject = subject
        self.files_source_txt = f'{util.resource_path()}/{file_path}/{files_source}.txt'
        self.files_source_html = f'{util.resource_path()}/{file_path}/{files_source}.html'
        self.cfg_name = f"{util.resource_path()}/config/{creds.Creds.cfg_name}.ini"
        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.cfg_name)
        self.sender_email = self.cfg['settings']['sender_email']
        self.password = self.cfg['settings']['sender_email_password']
        self.test_email = self.cfg['settings']['test_email']
        self.send_to = ""
        self.rec_list = []

    def build_and_send(self, to_addrs=None, host="smtp.gmail.com", port=465, write_output=True, conn_test=False):
        # build
        if to_addrs is None:
            to_addrs = self.test_email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = self.subject
        msg["From"] = self.sender_email
        msg["To"] = to_addrs
        msg["Bcc"] = ""

        # test Airtable connection
        if conn_test:
            try:
                with open(self.files_source_txt, "r") as t:
                    text = t.read()
                test_part = MIMEText(text, "plain")
                msg.attach(test_part)
                with smtplib.SMTP_SSL(host, port, context=self.context) as server:
                    server.login(self.sender_email, self.password)
                    return msg
            except FileNotFoundError:
                return ""

        # send mail
        try:
            with open(self.files_source_txt, "r") as t:
                text = t.read()
            with open(self.files_source_html, "r") as h:
                html = h.read()
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            msg.attach(part1)
            msg.attach(part2)
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

    def filter_list(self, client_list, write_output=True, output_path="/docs/outputs/"):
        for each in client_list:
            self.rec_list.append(each)
            self.build_and_send(each.email)
        filepath = Path()
        if write_output:
            output_list = output.Output(self.rec_list, path=output_path)
            filepath = output_list.write()
        return filepath
