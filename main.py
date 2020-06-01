from Email import Email
import requests
import os
import datetime
from Client import Client
from airtable import Airtable

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
    QListView, QGridLayout, QLineEdit, QComboBox
from PySide2.QtGui import Qt, QFont
from PySide2.QtCore import Qt, QStringListModel, Signal
import sys
import configparser
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


class Welcome(QWidget):

    switch = Signal(int)

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("SummitMailer")

        layout = QVBoxLayout()
        title = QLabel("SummitMail(er)")
        title.setAlignment(Qt.AlignCenter)
        font_title = QFont()
        font_title.setBold(True)
        font_title.setPointSize(72)
        font_title.setLetterSpacing(QFont.AbsoluteSpacing, -2.0)
        title.setFont(font_title)
        subtitle = QLabel("send mass email campaigns with Airtable API")
        subtitle.setAlignment(Qt.AlignCenter)
        font_subtitle = QFont()
        font_subtitle.setPointSize(12)
        subtitle.setFont(font_subtitle)

        font_subtitle.setPointSize(14)
        btn_saved_cfg = QPushButton("Start from saved cfg")
        btn_new_session = QPushButton("Start new session")
        btn_saved_cfg.setFont(font_subtitle)
        btn_new_session.setFont(font_subtitle)
        btn_saved_cfg.setFixedSize(150, 80)
        btn_new_session.setFixedSize(150, 80)

        btn_group = QHBoxLayout()
        btn_group.setContentsMargins(25, 25, 25, 25)
        btn_group.addWidget(btn_saved_cfg)
        btn_group.addWidget(btn_new_session)
        btn_group.setAlignment(Qt.AlignCenter)

        btn_saved_cfg.clicked.connect(lambda: self.switch_window(1))
        btn_new_session.clicked.connect(lambda: self.switch_window(2))

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(btn_group)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.addStretch(1)

        self.setLayout(layout)
        self.setGeometry(311, 186, 817, 330)

    def switch_window(self, num):
        self.switch.emit(num)


class LoadFromSaved(QWidget):

    switch = Signal(int)

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Load from saved cfg")

        layout = QVBoxLayout()
        # widget 1: prompt
        font = QFont()
        font.setPointSize(14)
        prompt = QLabel("Choose a configuration to load")
        prompt.setAlignment(Qt.AlignCenter)
        prompt.setFont(font)
        prompt.setContentsMargins(25, 25, 25, 25)
        # widget 2: list
        """model = QStringListModel(["cfg1", "cfg2", "cfg3", "..."])
        list_view = QListView()
        list_view.setFont(font)
        list_view.setModel(model)"""
        self.list_cfgs = QComboBox()
        self.list_cfgs.setStyleSheet("color: white")
        for cfg in os.listdir('Cfg'):
            self.list_cfgs.addItem(cfg)
        self.list_cfgs.currentIndexChanged.connect(self.cfg_selection())
        # widget 3: next/back buttons
        btn_group = QHBoxLayout()
        back = QPushButton("Back")
        go = QPushButton("Go")
        btn_group.addWidget(back)
        btn_group.addWidget(go)
        back.clicked.connect(lambda: self.switch_window(0))
        # add widgets
        layout.addWidget(prompt)
        layout.addWidget(self.list_cfgs)
        layout.addLayout(btn_group)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 400, 180)

    def switch_window(self, num):
        self.switch.emit(num)

    def cfg_selection(self):
        # this function will initiate airtable class with selected cfg
        print(self.list_cfgs.count())


class Load_newSession(QWidget):

    switch = Signal(int)

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Load new cfg")

        layout = QVBoxLayout()
        # widget 1: edit lines
        base_id = QLabel("Base ID")
        api_key = QLabel("API Key")
        edit_base_id = QLineEdit()
        edit_api_key = QLineEdit()
        # setup grid layout
        layout_grid = QGridLayout()
        layout_grid.setSpacing(10)
        layout_grid.addWidget(base_id, 1, 0)
        layout_grid.addWidget(edit_base_id, 1, 1)
        layout_grid.addWidget(api_key, 2, 0)
        layout_grid.addWidget(edit_api_key, 2, 1)
        # widget 2: buttons
        btn_group = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_save = QPushButton("Save cfg")
        btn_use_once = QPushButton("Use Once")
        btn_group.addWidget(btn_back)
        btn_group.addWidget(btn_save)
        btn_group.addWidget(btn_use_once)
        btn_back.clicked.connect(lambda: self.switch_window(0))
        # add all layouts
        layout.addLayout(layout_grid)
        layout.addLayout(btn_group)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 400, 180)

    def switch_window(self, num):
        self.switch.emit(num)


class Controller:

    def __init__(self):
        pass

    def loader(self, num):
        if num == 0:
            self.show_welcome()
            try:
                if self.load_cfg:
                    self.load_cfg.close()
                if self.load_new:
                    self.load_new.close()
            except AttributeError:
                pass
        if num == 1:
            self.show_load_cfg()
        if num == 2:
            self.show_load_new()

    def show_welcome(self):
        self.welcome = Welcome()
        self.welcome.switch.connect(self.loader)
        self.welcome.show()

    def show_load_cfg(self):
        self.load_cfg = LoadFromSaved()
        self.load_cfg.switch.connect(self.loader)
        self.welcome.close()
        self.load_cfg.show()

    def show_load_new(self):
        self.load_new = Load_newSession()
        self.load_new.switch.connect(self.loader)
        self.welcome.close()
        self.load_new.show()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("SummitMailer")
    app.setStyle("Fusion")
    controller = Controller()
    controller.show_welcome()
    sys.exit(app.exec_())
