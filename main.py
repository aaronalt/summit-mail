from Email import Email
import requests
import os
import datetime
from Client import Client
from airtable import Airtable

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
    QListView, QGridLayout, QLineEdit
from PySide2.QtGui import Qt, QFont
from PySide2.QtCore import Qt, QStringListModel, Signal, Slot
import sys
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
        self.page_num = 0

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

        st.setPointSize(14)
        saved_cfg_btn = QPushButton("Start from saved cfg")
        new_session_btn = QPushButton("Start new session")
        saved_cfg_btn.setFont(st)
        new_session_btn.setFont(st)
        saved_cfg_btn.setFixedSize(150, 80)
        new_session_btn.setFixedSize(150, 80)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(25, 25, 25, 25)
        btn_layout.addWidget(saved_cfg_btn)
        btn_layout.addWidget(new_session_btn)
        btn_layout.setAlignment(Qt.AlignCenter)

        saved_cfg_btn.clicked.connect(self.switch_window_saved())
        new_session_btn.clicked.connect(self.switch_window_new())

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(btn_layout)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.addStretch(1)

        window = QWidget()
        self.setLayout(layout)
        self.setGeometry(311, 186, 817, 330)

    def switch_window_saved(self):
        self.page_num = 1
        self.switch.emit(self.page_num)

    def switch_window_new(self):
        self.page_num = 2
        self.switch.emit(self.page_num)


class LoadFromSaved(QWidget):

    switch = Signal()

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
        model = QStringListModel(["cfg1", "cfg2", "cfg3", "..."])
        list_view = QListView()
        list_view.setFont(font)
        list_view.setModel(model)
        # widget 3: next/back buttons
        btns = QHBoxLayout()
        back = QPushButton("Back")
        go = QPushButton("Go")
        btns.addWidget(back)
        btns.addWidget(go)
        # back.clicked.connect()
        # add widgets
        layout.addWidget(prompt)
        layout.addWidget(list_view)
        layout.addLayout(btns)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 400, 180)


class LoadNewSession(QWidget):

    switch = Signal()

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
        layout_btns = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_save = QPushButton("Save cfg")
        btn_use_once = QPushButton("Use Once")
        layout_btns.addWidget(btn_back)
        layout_btns.addWidget(btn_save)
        layout_btns.addWidget(btn_use_once)
        # add all layouts
        layout.addLayout(layout_grid)
        layout.addLayout(layout_btns)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 400, 180)


class Controller:

    def __init__(self):
        pass

    def show_welcome(self):
        self.welcome = Welcome()
        self.welcome.switch.connect(self.cfg)
        self.welcome.show()

    @Slot()
    def cfg(self, num):
        print(num)

    def show_loadCfg(self):
        self.loadCfg = LoadFromSaved()
        #self.loadCfg.switch.connect()
        self.welcome.close()
        self.loadCfg.show()

    def show_loadNew(self):
        self.loadNew = LoadNewSession()
        self.welcome.close()
        self.loadNew.show()

if __name__ == '__main__':
    # main()
    app = QApplication([])
    app.setApplicationName("SummitMailer")
    app.setStyle("Fusion")
    controller = Controller()
    controller.show_welcome()
    sys.exit(app.exec_())
