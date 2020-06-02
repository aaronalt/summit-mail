import os
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
    QListView, QGridLayout, QLineEdit, QComboBox, QProgressBar, QTableView
from PySide2.QtGui import Qt, QFont
from PySide2.QtCore import Qt, QStringListModel, Signal
import sys
import configparser

from PySide2.examples.widgets.itemviews.addressbook.tablemodel import TableModel
from dotenv import load_dotenv
load_dotenv()


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
        prompt.setContentsMargins(5, 5, 5, 5)
        # widget 2: list
        self.list_cfgs = QComboBox()
        self.list_cfgs.setContentsMargins(5, 5, 5, 5)
        self.list_cfgs.setStyleSheet("color: white")
        for cfg in os.listdir('Cfg'):
            self.list_cfgs.addItem(cfg)
        self.list_cfgs.currentIndexChanged.connect(self.cfg_selection())
        # widget 3: next/back buttons
        btn_group = QHBoxLayout()
        btn_group.setContentsMargins(5, 20, 5, 5)
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


class LoadNewSession(QWidget):

    switch = Signal(int)
    cfg_name = ''
    api_key = ''
    base_id = ''

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Load new cfg")

        layout = QVBoxLayout()
        # widget 1: edit lines
        base = QLabel("Base ID")
        apikey = QLabel("API Key")
        cfg_name = QLabel("Name")
        edit_base_id = QLineEdit()
        edit_api_key = QLineEdit()
        edit_cfg_name = QLineEdit()
        edit_base_id.editingFinished.connect(lambda: self.set_base(edit_base_id.text()))
        edit_api_key.editingFinished.connect(lambda: self.set_key(edit_api_key.text()))
        edit_cfg_name.editingFinished.connect(lambda: self.set_name(edit_cfg_name.text()))
        # setup grid layout
        layout_grid = QGridLayout()
        layout_grid.setSpacing(10)
        layout_grid.addWidget(cfg_name, 1, 0)
        layout_grid.addWidget(edit_cfg_name, 1, 1)
        layout_grid.addWidget(base, 2, 0)
        layout_grid.addWidget(edit_base_id, 2, 1)
        layout_grid.addWidget(apikey, 3, 0)
        layout_grid.addWidget(edit_api_key, 3, 1)
        # widget 2: buttons
        btn_group = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_save = QPushButton("Save cfg")
        btn_use_once = QPushButton("Use Once")
        btn_group.addWidget(btn_back)
        btn_group.addWidget(btn_save)
        btn_group.addWidget(btn_use_once)
        btn_back.clicked.connect(lambda: self.switch_window(0))
        btn_save.clicked.connect(self.save_cfg)
        # add all layouts
        layout.addLayout(layout_grid)
        layout.addLayout(btn_group)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 400, 180)

    def switch_window(self, num):
        self.switch.emit(num)

    def set_base(self, text):
        self.base_id = text

    def set_key(self, text):
        self.api_key = text

    def set_name(self, text):
        self.cfg_name = text

    def save_cfg(self):
        cfg = configparser.ConfigParser()
        cfg['ENV'] = {'airtable_api_key': self.api_key,
                      'airtable_base_id': self.base_id}
        with open(f'Cfg/{self.cfg_name}.ini', 'w') as configfile:
            cfg.write(configfile)


class Controller:

    def __init__(self):
        pass

    def loader(self, num):
        if num == 0:
            try:
                if self.load_cfg:
                    self.load_cfg.close()
            except AttributeError:
                if self.load_new:
                    self.load_new.close()
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
        self.load_cfg.show()

    def show_load_new(self):
        self.load_new = LoadNewSession()
        self.load_new.switch.connect(self.loader)
        self.load_new.show()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("SummitMailer")
    app.setStyle("Fusion")
    controller = Controller()
    controller.show_welcome()
    sys.exit(app.exec_())
