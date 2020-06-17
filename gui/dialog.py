from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox


class Dialog(QDialog):

    def __init__(self, message=""):
        super().__init__()
        self.message = message
        layout = QVBoxLayout()
        dialog = QDialog(self)
        label_notice = QLabel(message)
        btn_ok = QDialogButtonBox(QDialogButtonBox.Ok)
        layout.addWidget(label_notice)
        layout.addWidget(btn_ok)
        dialog.setGeometry(511, 380, 200, 100)
        dialog.setLayout(layout)
        btn_ok.accepted.connect(dialog.accept)
        dialog.exec_()
