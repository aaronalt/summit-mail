import os
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QLineEdit, QComboBox, QProgressBar, QTableView, QHeaderView, QAbstractScrollArea, QDialog, \
    QDialogButtonBox
from PySide2.QtGui import Qt, QFont
from PySide2.QtCore import Qt, Signal, QAbstractTableModel
import sys
import configparser

from PySide2.examples.widgets.itemviews.addressbook.tablemodel import TableModel
from SummitMail import SummitMail
from Output import Output


class Creds:

    def __init__(self, base_id, api_key, cfg_name):
        self.base_id = base_id
        self.api_key = api_key
        self.cfg_name = cfg_name

    @property
    def base_id(self):
        print("getting base_id...")
        return self._base_id

    @base_id.setter
    def base_id(self, value):
        print("setting base_id")
        self._base_id = value

    @property
    def api_key(self):
        print("getting api_key...")
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        print("setting api_key...")
        self._api_key = value

    @property
    def cfg_name(self):
        print("getting cfg_name...")
        return self._cfg_name

    @cfg_name.setter
    def cfg_name(self, value):
        print("setting cfg_name...")
        self._cfg_name = value


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
    # todo: add table name field from user input
    # table_name = ''

    def __init__(self, base_id='', api_key='', cfg_name=''):
        QWidget.__init__(self)
        self.setWindowTitle("Load from saved cfg")
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
        for cfg in os.listdir('Cfg'):
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
        self.switch.emit(num)

    def cfg_selection(self, item):
        """ this function will create an .ini file with env variables stored from user input"""
        print(item)
        cfg = configparser.ConfigParser()
        cfg.read(os.path.join('Cfg/', item))
        try:
            assert(cfg['ENV']['airtable_base_id'])
            assert(cfg['ENV']['airtable_api_key'])
            assert (cfg['ENV']['cfg_name'])
        except AssertionError as ae:
            # put dialog box here for error
            print(f"\nAssertionError: No ENV variable {ae}\n")
        except KeyError as ke:
            print(f"\nKeyError: No ENV variable {ke}\n")
        self.api_key = cfg['ENV']['airtable_api_key']
        self.base_id = cfg['ENV']['airtable_base_id']
        self.cfg_name = cfg['ENV']['cfg_name']

    def set_airtable_creds(self):
        """ this function will send credentials to MainWindow class in order to init Airtable """
        print("loading main app...")
        # todo: input for 'table name' and ensuing functionality {integrate list of table names in cfg}

        creds = Creds(self.base_id, self.api_key, self.cfg_name)
        return creds


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
        btn_use_once = QPushButton("Use once")
        btn_group.addWidget(btn_back)
        btn_group.addWidget(btn_save)
        btn_group.addWidget(btn_use_once)
        btn_back.clicked.connect(lambda: self.switch_window(0))
        # todo: add dialog for when 'saved' is clicked
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

    def save_cfg(self):
        cfg = configparser.ConfigParser()
        cfg['ENV'] = {'cfg_name': self.cfg_name,
                      'airtable_api_key': self.api_key,
                      'airtable_base_id': self.base_id}
        with open(f'Cfg/{self.cfg_name}.ini', 'w') as configfile:
            cfg.write(configfile)

    def set_airtable_creds(self):
        """ this function will send credentials to MainWindow class in order to init Airtable """
        print("loading main app from new cfg...")
        creds = Creds(self.base_id, self.api_key, self.cfg_name)
        return creds


class LoadMainWindow(QWidget):

    switch = Signal(int)
    data = list()
    client_objects = list()

    def __init__(self, base_id, api_key, cfg_name, base_name="New Contacts"):
        QWidget.__init__(self)
        self.base_id = base_id
        self.api_key = api_key
        self.cfg_name = cfg_name
        self.base_name = base_name
        self.setWindowTitle("SummitMailer")

        layout = QVBoxLayout()
        # widget group 1: collect, run, progress bar, base name
        btn_group_collect_run_progress = QHBoxLayout()
        btn_collect = QPushButton("Collect")
        btn_run = QPushButton("Run")
        progress = QProgressBar()
        progress.setOrientation(Qt.Horizontal)
        label_base = QLabel(self.base_name)
        btn_group_collect_run_progress.addWidget(btn_collect)
        btn_group_collect_run_progress.addWidget(btn_run)
        btn_group_collect_run_progress.addWidget(progress)
        btn_group_collect_run_progress.addWidget(label_base)
        btn_collect.clicked.connect(self.collect_data)
        # widget group 2: table
        """
        access airtable here:
        # data = [
        #         ["Company1", "country", "website", "etc."],
        #     ]
        table_model = TableModel(data)
        """
        table = QHBoxLayout()
        self.table_model = TableModel(self.data)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.addWidget(self.table_view)
        # widget group 3: test/edit html
        btn_group_edit_test = QHBoxLayout()
        btn_generate_output = QPushButton("generate output")
        btn_send_test = QPushButton("send test")
        label_view_edit = QLabel("view/edit:")
        btn_edit_html = QPushButton("html")
        btn_edit_txt = QPushButton("txt")
        btn_group_edit_test.addWidget(btn_generate_output)
        btn_group_edit_test.addWidget(btn_send_test)
        btn_group_edit_test.addWidget(label_view_edit)
        btn_group_edit_test.addWidget(btn_edit_html)
        btn_group_edit_test.addWidget(btn_edit_txt)
        btn_generate_output.clicked.connect(self.generate_output)
        # add layouts
        layout.addLayout(btn_group_collect_run_progress)
        layout.addLayout(table)
        layout.addLayout(btn_group_edit_test)
        # setup window
        self.setLayout(layout)
        self.setGeometry(311, 186, 817, 600)

    def test_call(self):
        connect = SummitMail(self.base_id, self.api_key)
        return connect

    def collect_data(self):
        """ connect to AirTable; return data before sending """
        airtable = SummitMail(self.base_id, self.api_key)
        self.client_objects = airtable.daily_25()
        for c in self.client_objects:
            client = [c.name, c.country, c.website, c.email]
            self.data.append(client)
        self.table_model.layoutChanged.emit()
        self.table_view.resizeColumnsToContents()
        return self.table_model

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
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setLayout(layout)
        btn_ok.accepted.connect(dialog.accept)
        dialog.exec_()


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        try:
            len(self._data) == 0
        except IndexError as e:
            return 0
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        try:
            len(self._data[0]) == 0
        except IndexError as e:
            return 0
        return len(self._data[0])


class Controller:

    def __init__(self):
        pass

    def loader(self, num):
        try:
            self.load_cfg.close()
            self.load_new.close()
        except AttributeError:
            pass
        finally:
            if num == 0:
                print("num=0")
            if num == 1:
                self.show_load_cfg()
            if num == 2:
                self.show_load_new()
            if num == 3:
                creds = self.load_cfg.set_airtable_creds()
                self.show_load_main(creds.base_id, creds.api_key, creds.cfg_name)
            if num == 4:
                creds = self.load_new.set_airtable_creds()
                # todo: add more specific exceptions
                try:
                    self.show_load_main(creds.base_id, creds.api_key, creds.cfg_name)
                    self.load_main.test_call()
                except KeyError:
                    print("credentials provided do not match existing")
                finally:
                    self.load_main.close()

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

    def show_load_main(self, base_id, api_key, cfg_name):
        self.load_main = LoadMainWindow(base_id, api_key, cfg_name)
        self.load_main.switch.connect(self.loader)
        self.load_main.show()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("SummitMailer")
    app.setStyle("Fusion")
    controller = Controller()
    controller.show_welcome()
    sys.exit(app.exec_())
