from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import pickle


class UpdateWindow(QDialog):
    def __init__(self, item):
        super().__init__()

        self.item = item
        self.setWindowTitle("Update Window")
        self.setGeometry(100, 100, 300, 400)
        self.formGroupBox = QGroupBox("Form 1")
        self.usernameLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()
        self.websiteLineEdit = QLineEdit()
        self.nameLineEdit = QLineEdit()

        self.createForm(item)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.update)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def update(self):
        if os.path.exists("database.pkl"):
            with open("database.pkl", "rb") as f:
                datadict = pickle.load(f)

            datadict[self.item.text()]["username"] = self.usernameLineEdit.text()
            datadict[self.item.text()]["password"] = self.passwordLineEdit.text()
            datadict[self.item.text()]["website"] = self.websiteLineEdit.text()

            with open("database.pkl", "wb") as f:
                pickle.dump(datadict, f)

        self.close()

    def createForm(self, item):
        layout = QFormLayout()
        layout.addRow(QLabel("Username:"), self.usernameLineEdit)
        layout.addRow(QLabel("Password:"), self.passwordLineEdit)
        layout.addRow(QLabel("Website:"), self.websiteLineEdit)

        if os.path.exists("database.pkl"):
            with open("database.pkl", "rb") as f:
                datadict = pickle.load(f)

            self.usernameLineEdit.setText(datadict[item.text()]["username"])
            self.passwordLineEdit.setText(datadict[item.text()]["password"])
            self.websiteLineEdit.setText(datadict[item.text()]["website"])

        self.formGroupBox.setLayout(layout)
