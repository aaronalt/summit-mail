from Email import Email
import requests
import os
import datetime
from Client import Client
from airtable import Airtable

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide2.QtGui import Qt, QFont
from PySide2.QtCore import Qt

from dotenv import load_dotenv
load_dotenv()


"""class SummitMail:
    d = datetime.datetime.now()
    date = f'{d.day}/{d.month}/{d.year}'

    new_contacts = Airtable('appTpBROWIBsmE7FD', "New Contacts", api_key=os.getenv("AIRTABLE_API_KEY"))
    countries_table = Airtable('appTpBROWIBsmE7FD', "Countries", api_key=os.getenv("AIRTABLE_API_KEY"))
    all_countries = countries_table.get_all()
    client_objects = []

    for id in new_contacts.get_all(formula="{status}=''", max_records=25):
        # update country field with string from record id
        country = ''
        for i in all_countries:
            if i['id'] == id['fields']['country'][0]:
                country = i['fields']['Name']
                break
        new_client = Client('', '', '', '')
        try:
            new_client = Client(id['fields']['name'].strip(), country,
                                id['fields']['website'],
                                id['fields']['email'].strip())
            client_objects.append(new_client)
            record = new_contacts.match('name', new_client.name)
            fields = {'name': new_client.name, 'country': new_client.country, 'website': new_client.website,
                      'email': new_client.email, 'status': 'Contacted', 'contact date': date, 'contact method': 'Email',
                      'source': 'goodfirms.co', 'result': 'No response'}
            new_contacts.update(record['id'], fields, typecast=True)
        except KeyError as error:
            print(f"There was a problem processing \'{id['fields']['name']}\'...")
            print(error)
            continue

    email = Email("App Development Support", "Inputs/contact_new_clients")
    email.send_external(client_objects)"""


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow).__init__(*args, **kwargs)
        layout = QVBoxLayout()

        title = QLabel("SummitMail(er)")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(72)
        title_font.setLetterSpacing(QFont.AbsoluteSpacing, -2.0)
        title.setFont(title_font)

        subtitle = QLabel("send mass email campaigns with Airtable API")
        subtitle.setAlignment(Qt.AlignCenter)
        st = QFont()
        st.setPointSize(12)
        subtitle.setFont(st)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(25, 50, 25, 25)
        saved_cfg_btn = QPushButton("Start from saved cfg")
        new_session_btn = QPushButton("Start new session")
        btn_layout.addWidget(saved_cfg_btn)
        btn_layout.addWidget(new_session_btn)
        btn_layout.setAlignment(Qt.AlignCenter)
        # btn_layout.addStretch(1)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(btn_layout)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.addStretch(1)

        window = QWidget()
        window.setLayout(layout)
        window.setGeometry(311, 186, 817, 529)
        window.show()
        app.exec_()


# def main():
    # mailer = SummitMail()


if __name__ == '__main__':
    # main()
    app = QApplication([])
    app.setApplicationName("SummitMailer")
    app.setStyle("Fusion")
    MainWindow()
