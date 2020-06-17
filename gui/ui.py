import configparser
import os
from queue import Queue
from threading import Thread

from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QLineEdit, QGridLayout, \
    QTableView, QAbstractScrollArea, QDialog, QDialogButtonBox
from PySide2.examples.widgets.itemviews.addressbook.tablemodel import TableModel

from Email import Email
from Output import Output
from SummitMail import SummitMail
from gui.creds import Creds
from gui.dialog import Dialog


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
        btn_saved_cfg = QPushButton("Start from saved Cfg")
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


class FromSaved(QWidget):

    switch = Signal(int, object)

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
        for cfg in os.listdir('../Cfg'):
            self.list_cfgs.addItem(cfg)
        self.list_cfgs.activated[str].connect(self.cfg_selection)
        # widget 3: next/back buttons
        btn_group = QHBoxLayout()
        btn_group.setContentsMargins(5, 20, 5, 5)
        back = QPushButton("Back")
        go = QPushButton("Go")
        btn_group.addWidget(back)
        btn_group.addWidget(go)
        back.clicked.connect(lambda: self.switch_window(0))
        go.clicked.connect(lambda: self.switch_window(3))
        # add widgets
        layout.addWidget(prompt)
        layout.addWidget(self.list_cfgs)
        layout.addLayout(btn_group)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 400, 180)

    def switch_window(self, num):
        self.switch.emit(num, Creds)

    def cfg_selection(self, item):
        """ this function will create an .ini file with env variables stored from user input"""
        print(item)
        cfg = configparser.ConfigParser()
        cfg.read(os.path.join('../Cfg/', item))
        try:
            assert (cfg['ENV']['airtable_base_id'])
            assert (cfg['ENV']['airtable_api_key'])
            assert (cfg['ENV']['cfg_name'])
        except AssertionError as ae:
            # put dialog box here for error
            print(f"\nAssertionError: No ENV variable {ae}\n")
        except KeyError as ke:
            print(f"\nKeyError: No ENV variable {ke}\n")
        Creds.api_key = cfg['ENV']['airtable_api_key']
        Creds.base_id = cfg['ENV']['airtable_base_id']
        Creds.cfg_name = cfg['ENV']['cfg_name']

    def set_airtable_creds(self):
        # todo: input for 'table name' and ensuing functionality {integrate list of table names in Cfg}
        creds = Creds(self.base_id, self.api_key, self.cfg_name)
        return creds


class FromNew(QWidget):

    switch = Signal(int)
    api_key = str()
    base_id = str()
    sender_email = str()
    sender_email_pw = str()
    test_email = str()
    cfg_name = str()

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Load new Cfg")
        layout = QVBoxLayout()
        # widget 1: edit lines
        base = QLabel("Base ID")
        apikey = QLabel("API Key")
        cfg_name = QLabel("Name")
        label_sender = QLabel("Sender Email")
        label_sender_pw = QLabel("Email Password")
        label_test_email = QLabel("Test Email")
        edit_base_id = QLineEdit()
        edit_api_key = QLineEdit()
        edit_cfg_name = QLineEdit()
        edit_sender_email = QLineEdit()
        edit_sender_email_pw = QLineEdit()
        edit_test_email = QLineEdit()
        edit_base_id.editingFinished.connect(lambda: self.set_base(edit_base_id.text()))
        edit_api_key.editingFinished.connect(lambda: self.set_key(edit_api_key.text()))
        edit_cfg_name.editingFinished.connect(lambda: self.set_name(edit_cfg_name.text()))
        edit_sender_email.editingFinished.connect(lambda: self.set_sender_email(edit_sender_email.text()))
        edit_sender_email_pw.editingFinished.connect(lambda: self.set_sender_email_pw(edit_sender_email_pw.text()))
        edit_test_email.editingFinished.connect(lambda: self.set_test_email(edit_test_email.text()))
        # setup grid layout
        layout_grid = QGridLayout()
        layout_grid.setSpacing(10)
        layout_grid.addWidget(cfg_name, 1, 0)
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
        btn_back.clicked.connect(lambda: self.switch_window(0))
        btn_save.clicked.connect(self.save_cfg)
        btn_use_once.clicked.connect(lambda: self.switch_window(4))
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

    def set_sender_email(self, text):
        self.sender_email = text

    def set_sender_email_pw(self, text):
        self.sender_email_pw = text

    def set_test_email(self, text):
        self.test_email = text

    def save_cfg(self):
        cfg = configparser.ConfigParser()
        cfg['ENV'] = {'cfg_name': self.cfg_name,
                      'airtable_api_key': self.api_key,
                      'airtable_base_id': self.base_id}
        cfg['settings'] = {'sender_email': self.sender_email,
                           'sender_email_password': self.sender_email_pw,
                           'test_email': self.test_email}
        with open(f'../Cfg/{self.cfg_name}.ini', 'w') as configfile:
            cfg.write(configfile)
        dialog = Dialog("Cfg saved!")
        return dialog

    def set_airtable_creds(self):
        """ this function will send credentials to MainWindow class in order to init Airtable """
        print("loading main app from new Cfg...")
        creds = Creds(self.base_id, self.api_key, self.cfg_name)
        return creds


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
        btn_generate_output.clicked.connect(self.generate_output)
        # add layouts
        layout.addLayout(btn_group_collect_run_progress)
        layout.addLayout(table)
        layout.addLayout(btn_group_edit_test)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 817, 600)

    def test_call(self):
        connect = SummitMail(self.base_id, self.api_key, self.cfg_name)
        return connect

    def collect_data(self):
        """ connect to AirTable; return data before sending """
        airtable = SummitMail(self.base_id, self.api_key, self.cfg_name)
        self.client_objects = airtable.daily_25()
        for c in self.client_objects:
            client = [c.name, c.country, c.website, c.email]
            self.data.append(client)
        self.table_model.layoutChanged.emit()
        self.table_view.resizeColumnsToContents()
        return self.table_model

    def run(self):
        airtable = SummitMail(self.base_id, self.api_key, self.cfg_name)
        clients = airtable.daily_25(update=True)
        source = f'Inputs/{self.files_source}'
        if not os.path.exists(source + '.txt') | os.path.exists(source + '.html'):
            dialog = Dialog("Invalid file source")
            return dialog
        else:
            send_emails = airtable.send_to_all(self.subject, self.files_source, clients)
            dialog = Dialog(send_emails)
            return dialog

    def generate_output(self):
        if self.data:
            output = Output(self.client_objects)
            path, filename = output.write()
            output_filename = os.path.join(path, filename)
            self.output_dialog(output_filename)
        else:
            self.output_dialog("")

    def output_dialog(self, path_or_nodata):
        # todo: load generated output file instead of path
        layout = QVBoxLayout()
        dialog = QDialog(self)
        label_notice = QLabel()
        if path_or_nodata:
            label_notice = QLabel(f"Output generated at:\n{path_or_nodata}", dialog)
        else:
            label_notice = QLabel("No data to write", dialog)
        label_notice.setMargin(25)
        btn_ok = QDialogButtonBox(QDialogButtonBox.Ok)
        layout.addWidget(label_notice)
        layout.addWidget(btn_ok)
        dialog.setGeometry(511, 380, 200, 100)
        dialog.setLayout(layout)
        btn_ok.accepted.connect(dialog.accept)
        dialog.exec_()

    def before_send_dialog(self):
        # todo: add checkbox for 'update table' clicked by default
        # todo: add progress bar for sending test/all
        layout_grid = QGridLayout()
        label_subject = QLabel("Subject")
        label_files_source = QLabel("Files Source")
        edit_subject = QLineEdit()
        edit_files_source = QLineEdit()
        edit_subject.editingFinished.connect(lambda: self.set_subject(edit_subject.text()))
        edit_files_source.editingFinished.connect(lambda: self.set_files_source(edit_files_source.text()))
        btn_edit = QPushButton("edit")
        btn_test = QPushButton("send test")
        btn_test.clicked.connect(self.send_test)
        dialog = QDialog(self)
        dialog.setGeometry(511, 380, 400, 150)
        btn_send = QDialogButtonBox(QDialogButtonBox.Apply)
        btn_back = QDialogButtonBox(QDialogButtonBox.Cancel)
        btn_back.clicked.connect(dialog.accept)
        btn_send.clicked.connect(self.run)
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

    def send_test(self):
        test = Email(self.subject, self.files_source, self.cfg_name)
        test_message = test.build_message()
        if test_message:
            test.send_test_once()
            dialog = Dialog("Test sent!")
            return dialog
        else:
            dialog = Dialog("Invalid file source: not found")
            return dialog