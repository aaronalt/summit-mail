from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QGridLayout, QPlainTextEdit, QWidget


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
        self.msg_detail = msg_detail = QPlainTextEdit(self)
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
        self.setup_ui()
        self.setWindowTitle(title)
        self.msg.setText(msg)
        self.msg_detail.setPlainText(msg_detail)
        self.msg_detail.setVisible(True)
        # todo: add show/hide details toggle, resize dialog
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

        """if not msg_detail:
            self.msg_detail_toggle.setVisible(False)"""