from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets
import os
import pickle
import utils


class SaveWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("注册信息")
        # save enough room for email
        self.setMinimumWidth(700)
        self.setWindowIcon(QtGui.QIcon(utils.card_file_box))
        self.formGroupBox = QGroupBox()

        self.usernameLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()
        self.websiteLineEdit = QLineEdit()
        self.nameLineEdit = QLineEdit()

        self.createForm()
        self.buttons = QDialogButtonBox(self)
        self.saveButton = self.buttons.addButton("保存", QDialogButtonBox.ActionRole)
        self.cancelButton = self.buttons.addButton("取消", QDialogButtonBox.RejectRole)
        self.saveButton.clicked.connect(self.saveregistration)
        self.cancelButton.clicked.connect(self.reject)

        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttons)
        self.setLayout(mainLayout)
        
        
    def createForm(self):
        layout = QFormLayout()
        
        radioBox = QGroupBox()
        layout.addRow(QLabel("账号"), radioBox)
        hbox = QHBoxLayout()
        self.googleAccount = QRadioButton("谷歌账号", self)
        self.googleAccount.toggled.connect(self.googleAction)
        self.nonGoogleAct = QRadioButton("非谷歌账号", self)
        self.nonGoogleAct.toggled.connect(self.nongoogleAction)
        self.nonGoogleAct.setChecked(True)
        hbox.addWidget(self.googleAccount)
        hbox.addWidget(self.nonGoogleAct)
        radioBox.setLayout(hbox)
        
        layout.addRow(QLabel("用户名/邮箱"), self.usernameLineEdit)
        layout.addRow(QLabel("密码"), self.passwordLineEdit)
        layout.addRow(QLabel("网址"), self.websiteLineEdit)
        layout.addRow(QLabel("给它命个名吧"), self.nameLineEdit)
        
        self.formGroupBox.setLayout(layout)
        
    
    def googleAction(self, selected):
        if selected:
            self.passwordLineEdit.setText("")
            self.passwordLineEdit.setDisabled(True)
            
    
    def nongoogleAction(self, selected):
        if selected:
            self.passwordLineEdit.setDisabled(False)
    
    
    def saveregistration(self):
        """Save a dictionary."""
        # check whether the file exists
        if os.path.exists(utils.database_file):
            with open(utils.database_file, "rb") as f:
                datadict = pickle.load(f)
        else:
            datadict = {}

        # check whether any entry is empty
        if self.googleAccount.isChecked():
            if (self.usernameLineEdit.text() != "" and
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
                
                QtWidgets.QMessageBox.information(self, "保存", "保存成功！")
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "注意", "您有未输入的信息，请重新输入")

                
        elif self.nonGoogleAct.isChecked():
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
                
                QtWidgets.QMessageBox.information(self, "保存", "保存成功！")
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "注意", "您有未输入的信息，请重新输入")
