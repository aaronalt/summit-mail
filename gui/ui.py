#! /usr/bin/env python3

import os
from queue import Queue
from threading import Thread

from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QLineEdit, QGridLayout, \
    QTableView, QAbstractScrollArea, QDialog, QDialogButtonBox
from PySide2.examples.widgets.itemviews.addressbook.tablemodel import TableModel

from gui.creds import Creds
from gui.models import TableModel
from actions.util import cfg_from_selection, cfg_api_key, cfg_base_id, cfg_name, cfg_sender_email, \
    cfg_sender_email_pw, cfg_test_email, save_cfg, send_test, generate_output, run
from actions.summitmail_to_airtable import SummitMail


def test_call():
    print('running test_call (ui.py)')
    sm = SummitMail(str(Creds.base_id))
    result = sm.test()
    return 1 if result else 0


class Listener(Thread):

    def __init__(self, listener):
        Thread.__init__(self)
        self.daemon = True
        self.listener, self.queue = listener, Queue()
        self._run = True
        self.start()

    def run(self):
        if self.listener is None:
            return
        while self._run:
            try:
                conn = self.listener.accept()
                msg = conn.recv()
                self.queue.put(msg)
            except:
                continue

    def close(self):
        self._run = False
        try:
            if self.listener is not None:
                self.listener.close()
        except:
            import traceback
            traceback.print_exc()


class Welcome(QWidget):

    switch = Signal(object, str)

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
        btn_saved_cfg = QPushButton("Start from saved Cfg")
        btn_new_session = QPushButton("Start new session")
        btn_saved_cfg.setFont(font_subtitle)
        btn_new_session.setFont(font_subtitle)
        btn_saved_cfg.setFixedSize(170, 60)
        btn_new_session.setFixedSize(150, 60)
        btn_group = QHBoxLayout()
        btn_group.setContentsMargins(25, 25, 25, 25)
        btn_group.addWidget(btn_saved_cfg)
        btn_group.addWidget(btn_new_session)
        btn_group.setAlignment(Qt.AlignCenter)
        btn_saved_cfg.clicked.connect(lambda: self.switch.emit(self, 'load_cfg'))
        btn_new_session.clicked.connect(lambda: self.switch.emit(self, 'load_new'))
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(btn_group)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.addStretch(1)
        self.setLayout(layout)
        self.setGeometry(311, 186, 517, 200)


class FromSaved(QWidget):

    switch = Signal(object, str)
    # todo: add table name field from user input
    # table_name = ''

    def __init__(self, base_id='', api_key='', cfg_name=''):
        QWidget.__init__(self)
        self.setWindowTitle("Load from saved Cfg")
        self.base_id = base_id
        self.api_key = api_key
        self.cfg_name = cfg_name
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
        for cfg in os.listdir('../config'):
            self.list_cfgs.addItem(cfg)
        self.list_cfgs.activated[str].connect(cfg_from_selection)
        # widget 3: next/back buttons
        btn_group = QHBoxLayout()
        btn_group.setContentsMargins(5, 20, 5, 5)
        back = QPushButton("Back")
        go = QPushButton("Go")
        btn_group.addWidget(back)
        btn_group.addWidget(go)
        back.clicked.connect(lambda: self.switch.emit(self, 'welcome'))
        go.clicked.connect(lambda: self.switch.emit(self, 'load_main'))
        # add widgets
        layout.addWidget(prompt)
        layout.addWidget(self.list_cfgs)
        layout.addLayout(btn_group)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 400, 180)


class FromNew(QWidget):

    switch = Signal(object, str)
    api_key = str()
    base_id = str()
    sender_email = str()
    sender_email_pw = str()
    test_email = str()

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Load new Cfg")
        layout = QVBoxLayout()
        # widget 1: edit lines
        base = QLabel("Base ID")
        apikey = QLabel("API Key")
        name = QLabel("Name")
        label_sender = QLabel("Sender Email")
        label_sender_pw = QLabel("Email Password")
        label_test_email = QLabel("Test Email")
        # todo: validation logic for empty fields
        edit_base_id = QLineEdit()
        edit_base_id.setPlaceholderText("Airtable Base ID, e.g. 'appXXXXXXX'")
        edit_api_key = QLineEdit()
        edit_api_key.setPlaceholderText("Airtable Api key, e.g. 'keyXXXXXXXX'")
        edit_cfg_name = QLineEdit("")
        edit_cfg_name.setPlaceholderText("Name your config")
        edit_sender_email = QLineEdit()
        edit_sender_email.setPlaceholderText("Email address to send from")
        edit_sender_email_pw = QLineEdit()
        edit_sender_email_pw.setPlaceholderText("Api password of sender email")
        edit_test_email = QLineEdit()
        edit_test_email.setPlaceholderText("Email address to test (try one of your own)")
        edit_base_id.editingFinished.connect(lambda: cfg_base_id(edit_base_id.text()))
        edit_api_key.editingFinished.connect(lambda: cfg_api_key(edit_api_key.text()))
        edit_cfg_name.editingFinished.connect(lambda: cfg_name(edit_cfg_name.text()))
        edit_sender_email.editingFinished.connect(lambda: cfg_sender_email(edit_sender_email.text()))
        edit_sender_email_pw.editingFinished.connect(lambda: cfg_sender_email_pw(edit_sender_email_pw.text()))
        edit_test_email.editingFinished.connect(lambda: cfg_test_email(edit_test_email.text()))
        # setup grid layout
        layout_grid = QGridLayout()
        layout_grid.setSpacing(10)
        layout_grid.addWidget(name, 1, 0)
        layout_grid.addWidget(edit_cfg_name, 1, 1)
        layout_grid.addWidget(base, 2, 0)
        layout_grid.addWidget(edit_base_id, 2, 1)
        layout_grid.addWidget(apikey, 3, 0)
        layout_grid.addWidget(edit_api_key, 3, 1)
        layout_grid.addWidget(label_sender, 4, 0)
        layout_grid.addWidget(edit_sender_email, 4, 1)
        layout_grid.addWidget(label_sender_pw, 5, 0)
        layout_grid.addWidget(edit_sender_email_pw, 5, 1)
        layout_grid.addWidget(label_test_email, 6, 0)
        layout_grid.addWidget(edit_test_email, 6, 1)
        # widget 2: buttons
        btn_group = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_save = QPushButton("Save Cfg")
        btn_use_once = QPushButton("Use once")
        btn_group.addWidget(btn_back)
        btn_group.addWidget(btn_save)
        btn_group.addWidget(btn_use_once)
        btn_back.clicked.connect(lambda: self.switch.emit(self, 'welcome'))
        btn_save.clicked.connect(save_cfg)
        btn_use_once.clicked.connect(lambda: self.switch.emit(self, 'load_main'))
        # add all layouts
        layout.addLayout(layout_grid)
        layout.addLayout(btn_group)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 400, 180)


class MainWindow(QWidget):

    switch = Signal(int)
    data = list()
    client_objects = list()
    subject = str()
    files_source = str()

    def __init__(self, base_name="New Contacts"):
        QWidget.__init__(self)
        self.base_id = Creds.base_id
        self.api_key = Creds.api_key
        self.cfg_name = Creds.cfg_name
        self.base_name = base_name
        self.airtable = SummitMail(str(Creds.base_id))
        self.setWindowTitle("SummitMailer")
        layout = QVBoxLayout()
        # widget group 1: collect, run, progress bar, base name
        btn_group_collect_run_progress = QGridLayout()
        btn_group_collect_run_progress.setSpacing(10)
        btn_group_collect_run_progress.setContentsMargins(0, 25, 10, 20)
        btn_collect = QPushButton("Collect")
        btn_run = QPushButton("Run")
        """progress = QProgressBar()
        progress.setOrientation(Qt.Horizontal)"""
        spacer = QWidget()
        label_base = QLabel(self.base_name)
        label_base.setAlignment(Qt.AlignRight)
        btn_group_collect_run_progress.addWidget(btn_collect, 1, 0)
        btn_group_collect_run_progress.addWidget(btn_run, 1, 1)
        btn_group_collect_run_progress.addWidget(spacer, 1, 2)
        btn_group_collect_run_progress.addWidget(label_base, 1, 4)
        btn_collect.clicked.connect(self.collect_data)
        btn_run.clicked.connect(self.before_send_dialog)
        # widget group 2: table
        table = QHBoxLayout()
        self.table_model = TableModel(self.data)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.addWidget(self.table_view)
        # widget group 3: test/edit html
        btn_group_edit_test = QGridLayout()
        btn_generate_output = QPushButton("generate output")
        label_view_edit = QLabel("view/edit:")
        label_view_edit.setAlignment(Qt.AlignRight)
        btn_edit_html = QPushButton("html")
        btn_edit_txt = QPushButton("txt")
        btn_group_edit_test.addWidget(btn_generate_output, 1, 0)
        btn_group_edit_test.addWidget(spacer, 1, 1)
        btn_group_edit_test.addWidget(spacer, 1, 2)
        btn_group_edit_test.addWidget(label_view_edit, 1, 3)
        btn_group_edit_test.addWidget(btn_edit_html, 1, 4)
        btn_group_edit_test.addWidget(btn_edit_txt, 1, 5)
        btn_generate_output.clicked.connect(lambda: generate_output(self.data, self.client_objects))
        # add layouts
        layout.addLayout(btn_group_collect_run_progress)
        layout.addLayout(table)
        layout.addLayout(btn_group_edit_test)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 817, 600)

    def collect_data(self):
        """
        Connect to Airtable; return data before sending

        :returns: table model change
        """
        self.client_objects = self.airtable.get_contacts_from_airtable()
        for c in self.client_objects:
            client = [c.name, c.country, c.website, c.email]
            self.data.append(client)
        self.table_model.layoutChanged.emit()
        self.table_view.resizeColumnsToContents()
        return self.table_model

    def before_send_dialog(self):
        # todo: add checkbox for 'update table' clicked by default
        layout_grid = QGridLayout()
        label_subject = QLabel("Subject")
        label_files_source = QLabel("Files Source")
        edit_subject = QLineEdit()
        edit_files_source = QComboBox()
        edit_files_source.setPlaceholderText("Choose file source...")
        edit_files_source.setStyleSheet("color: white")
        files_sources = []
        for source in os.listdir('../docs/inputs'):
            ext = source.find(".")
            new_source = source[:ext]
            if new_source not in files_sources:
                files_sources.append(new_source)
        edit_files_source.addItems(files_sources)
        edit_files_source.currentTextChanged.connect(self.set_files_source)
        edit_subject.editingFinished.connect(lambda: self.set_subject(edit_subject.text()))
        btn_edit = QPushButton("edit")
        btn_test = QPushButton("send test")
        btn_test.clicked.connect(lambda: send_test(self.subject, self.files_source))
        dialog = QDialog(self)
        dialog.setGeometry(511, 380, 400, 150)
        btn_send = QDialogButtonBox(QDialogButtonBox.Apply)
        btn_back = QDialogButtonBox(QDialogButtonBox.Cancel)
        btn_back.clicked.connect(dialog.accept)
        btn_send.clicked.connect(lambda: run(self.airtable, self.subject, self.files_source))
        layout_grid.addWidget(label_subject, 1, 0)
        layout_grid.addWidget(edit_subject, 1, 1)
        layout_grid.addWidget(label_files_source, 2, 0)
        layout_grid.addWidget(edit_files_source, 2, 1)
        layout_grid.addWidget(btn_edit, 3, 0)
        layout_grid.addWidget(btn_test, 3, 1)
        layout_grid.addWidget(btn_back, 4, 0)
        layout_grid.addWidget(btn_send, 4, 1)
        dialog.setLayout(layout_grid)
        dialog.exec_()

    def set_subject(self, text):
        print(f"subject set, \'{text}\'")
        self.subject = text

    def set_files_source(self, text):
        print(f"files_source set, \'{text}\'")
        self.files_source = text
