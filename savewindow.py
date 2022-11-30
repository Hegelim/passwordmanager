from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import pickle


class SaveWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("注册信息")
        self.formGroupBox = QGroupBox("注册信息")

        self.usernameLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()
        self.websiteLineEdit = QLineEdit()
        self.nameLineEdit = QLineEdit()

        self.createForm()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.saveregistration)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)
        
    def createForm(self):
        layout = QFormLayout()
        layout.addRow(QLabel("用户名:"), self.usernameLineEdit)
        layout.addRow(QLabel("密码:"), self.passwordLineEdit)
        layout.addRow(QLabel("网址:"), self.websiteLineEdit)
        layout.addRow(QLabel("给它命个名吧:"), self.nameLineEdit)
        self.formGroupBox.setLayout(layout)

    def saveregistration(self):
        """Save a dictionary."""
        # check whether the file exists
        if os.path.exists("database.pkl"):
            with open("database.pkl", "rb") as f:
                datadict = pickle.load(f)
        else:
            datadict = {}

        # check whether any entry is empty
        if (self.usernameLineEdit.text() != "" and
            self.passwordLineEdit.text() != "" and
            self.websiteLineEdit.text() != "" and
            self.nameLineEdit.text() != ""):

            newDict = {
                "username": self.usernameLineEdit.text(),
                "password": self.passwordLineEdit.text(),
                "website": self.websiteLineEdit.text(),
            }
            datadict[self.nameLineEdit.text()] = newDict

            with open('database.pkl', 'wb') as f:
                pickle.dump(datadict, f)

        else:
            self.show_warning_message_box()

        self.close()

    def show_warning_message_box(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("您有未输入的信息，请重新输入")
        self.msg.setWindowTitle("注意")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.exec_()
