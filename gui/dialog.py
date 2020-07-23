import os

from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QGridLayout, QPlainTextEdit, QWidget
from pathlib import Path


class Dialog(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        dialog = QDialog(self)
        btn_ok = QDialogButtonBox(QDialogButtonBox.Ok)
        layout.addWidget(btn_ok)
        dialog.setGeometry(511, 380, 200, 100)
        dialog.setLayout(layout)
        btn_ok.accepted.connect(dialog.reject)


class Message(QDialog):

    question_ = 0
    warning_ = 1
    error_ = 2
    info_ = 3
    task_ = 4

    def setup_ui(self):
        self.grid = grid = QGridLayout(self)
        grid.setObjectName("gridLayout")
        self.msg = msg = QLabel(self)
        msg.setWordWrap(True)
        msg.setObjectName("msg")
        grid.addWidget(msg, 0, 0, 1, 2)
        self.msg_detail = msg_detail = QPlainTextEdit(self.msg_from_file)
        msg_detail.setReadOnly(True)
        msg_detail.setObjectName("msgDetail")
        grid.addWidget(msg_detail, 1, 0, 1, 2)
        self.btn_box = btn_box = QDialogButtonBox(self)
        btn_box.setStandardButtons(QDialogButtonBox.Ok)
        btn_box.setObjectName("btnBox")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        grid.addWidget(btn_box, 3, 0, 1, 2)

    def __init__(self, type_of, title, msg, msg_detail='', default_yes=True, parent=None):
        QDialog.__init__(self, parent)
        self.msg_detail = msg_detail
        self.msg_from_file = ''
        self.is_path = msg_detail == Path(msg_detail)
        if self.is_path:
            with open(msg_detail, 'r+') as file:
                for line in file.readlines():
                    line = os.fspath(line)
                    self.msg_from_file += line
        self.setup_ui()
        self.setWindowTitle(title)
        self.msg.setText(msg)
        # todo: add show/hide details toggle
        # todo: resize dialog dynamically
        # self.msg_detail_toggle = self.btn_box.addButton()

        self.is_question = type_of == self.question_
        if self.is_question:
            self.btn_box.setStandardButtons(self.btn_box.Yes|self.btn_box.No)
            self.btn_box.button(self.btn_box.Yes if default_yes else self.btn_box.No).setDefault(True)
            self.default_yes = default_yes
        else:
            self.btn_box.button(self.btn_box.Ok).setDefault(True)

        self.is_error = type_of == self.error_
        if self.is_error:
            self.btn_box.rejected.connect(self.reject)

        self.is_warning = type_of == self.warning_
        if self.is_warning:
            self.grid.removeWidget(self.msg_detail)
            self.msg_detail.deleteLater()
            self.msg_detail = None

        self.is_info = type_of == self.info_
        if self.is_info:
            if not msg_detail:
                self.grid.removeWidget(self.msg_detail)
                self.msg_detail.deleteLater()
                self.msg_detail = None
        """if not msg_detail:
            self.msg_detail_toggle.setVisible(False)"""



