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
        self.layout = QFormLayout()
        
        radioBox = QGroupBox()
        self.layout.addRow(radioBox)
        hbox = QHBoxLayout()
        
        self.username = QLabel("邮箱/用户名")
        self.layout.addRow(self.username, self.usernameLineEdit)
        self.layout.addRow(QLabel("密码"), self.passwordLineEdit)    
        self.layout.addRow(QLabel("网址"), self.websiteLineEdit)
        self.layout.addRow(QLabel("给它命个名吧"), self.nameLineEdit)
        
        self.googleAccount = QRadioButton("谷歌账号登录", self)
        self.googleAccount.toggled.connect(self.googleAction)
        
        self.wechatAct = QRadioButton("微信登录", self)
        self.wechatAct.toggled.connect(self.wechatAction)
        
        self.otherAct = QRadioButton("自定义账号登录", self)
        self.otherAct.toggled.connect(self.otherAction)
        self.otherAct.setChecked(True)
        
        hbox.addWidget(self.googleAccount)
        hbox.addWidget(self.wechatAct)
        hbox.addWidget(self.otherAct)
        radioBox.setLayout(hbox)
        
        self.formGroupBox.setLayout(self.layout)
        
    def googleAction(self, selected):
        if selected:
            self.username.setText("谷歌邮箱")
            self.passwordLineEdit.setText("")
            self.passwordLineEdit.setDisabled(True)
            
            
    def wechatAction(self, selected):
        if selected:
            self.username.setText("微信账号")
            self.passwordLineEdit.setText("")
            self.passwordLineEdit.setDisabled(True)
    
    
    def otherAction(self, selected):
        if selected:
            self.username.setText("用户名/邮箱")
            self.passwordLineEdit.setDisabled(False)
    
    
    def getAct(self):
        if self.googleAccount.isChecked():
            return "google"
        elif self.wechatAct.isChecked():
            return "wechat"
        elif self.otherAct.isChecked():
            return "self-defined"
        else:
            return "none"
    
    
    def saveregistration(self):
        """Save a dictionary."""
        # check whether the file exists
        if os.path.exists(utils.database_file):
            with open(utils.database_file, "rb") as f:
                datadict = pickle.load(f)
        else:
            datadict = {}

        # check whether any entry is empty
        if self.googleAccount.isChecked() or self.wechatAct.isChecked():
            if (utils.isValidText(self.usernameLineEdit.text()) and
                utils.isValidText(self.websiteLineEdit.text()) and
                utils.isValidText(self.nameLineEdit.text())):
                                
                newDict = {
                    "account": self.getAct(),
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
                QtWidgets.QMessageBox.warning(self, "注意", "输入不能为空或含有空格")

                
        elif self.otherAct.isChecked():
            if (utils.isValidText(self.usernameLineEdit.text()) and
                utils.isValidText(self.passwordLineEdit.text())and
                utils.isValidText(self.websiteLineEdit.text()) and
                utils.isValidText(self.nameLineEdit.text())):
        
                newDict = {
                    "account": self.getAct(),
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
                QtWidgets.QMessageBox.warning(self, "注意", "输入不能为空或含有空格")
