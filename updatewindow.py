from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets
import os
import pickle
import utils


class UpdateWindow(QDialog):
    def __init__(self, parent, item):
        super().__init__(parent)

        self.item = item
        self.setWindowTitle("注册信息")
        self.setWindowIcon(QtGui.QIcon(utils.pen))
        self.formGroupBox = QGroupBox()
        self.usernameLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()
        self.websiteLineEdit = QLineEdit()
        self.nameLineEdit = QLineEdit()
        self.username = QLabel("用户名")

        self.readRegistration(item)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.update)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def update(self):
        """Modify registration and save"""
        if os.path.exists(utils.database_file):
            with open(utils.database_file, "rb") as f:
                datadict = pickle.load(f)

            if self.infoEmpty():
                QtWidgets.QMessageBox.warning(self, "更改", "输入不能为空或含有空格")
                
            elif self.infoNoChange(datadict):
                QtWidgets.QMessageBox.warning(self, "更改", "您未做任何更改")
                
            else:
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("更改")
                msg.setIcon(QMessageBox.Question)
                msg.setText(f"您要更新该信息")
                msg.setInformativeText("继续吗？")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                if msg.exec() == QMessageBox.Yes:
                    datadict[self.item.text()]['account'] = self.getAct()
                    datadict[self.item.text()]["username"] = self.usernameLineEdit.text()
                    datadict[self.item.text()]["password"] = self.passwordLineEdit.text()
                    datadict[self.item.text()]["website"] = self.websiteLineEdit.text()

                    with open(utils.database_file, "wb") as f:
                        pickle.dump(datadict, f)
                    
                    QtWidgets.QMessageBox.warning(self, "更改", "更改成功！")
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, "更改", "已取消更改")


    def readRegistration(self, item):
        """Read datadict and display registration information"""
        layout = QFormLayout()
        
        radioBox = QGroupBox()
        hbox = QHBoxLayout()
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
        
        layout.addRow(radioBox)
        
        layout.addRow(self.username, self.usernameLineEdit)
        layout.addRow(QLabel("密码"), self.passwordLineEdit)
        layout.addRow(QLabel("网址"), self.websiteLineEdit)

        if os.path.exists(utils.database_file):
            with open(utils.database_file, "rb") as f:
                datadict = pickle.load(f)

            # for older info, there is no account key
            if 'account' not in datadict[item.text()]:                
                self.googleAccount.setChecked(False)
                self.wechatAct.setChecked(False)
                self.otherAct.setChecked(False)
                self.usernameLineEdit.setText(datadict[item.text()]["username"])
                self.passwordLineEdit.setText(datadict[item.text()]["password"])
                self.websiteLineEdit.setText(datadict[item.text()]["website"])

            # for google account or wechat account, 
            # there is no password in registration
            elif datadict[item.text()]['account'] == "google":
                self.googleAccount.setChecked(True)
                self.usernameLineEdit.setText(datadict[item.text()]["username"])
                self.websiteLineEdit.setText(datadict[item.text()]["website"])
                
            elif datadict[item.text()]['account'] == "wechat":
                self.wechatAct.setChecked(True)
                self.usernameLineEdit.setText(datadict[item.text()]["username"])
                self.websiteLineEdit.setText(datadict[item.text()]["website"])
            
            elif datadict[item.text()]['account'] == "self-defined":
                self.otherAct.setChecked(True)
                self.usernameLineEdit.setText(datadict[item.text()]["username"])
                self.passwordLineEdit.setText(datadict[item.text()]["password"])
                self.websiteLineEdit.setText(datadict[item.text()]["website"])
            
        self.formGroupBox.setLayout(layout)


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


    def infoNoChange(self, datadict):
        """Return True if information in datadict does not change"""
        # if older registration has account information
        if 'account' in datadict[self.item.text()]:
            return (datadict[self.item.text()]["account"] == self.getAct() and
                    datadict[self.item.text()]["username"] == self.usernameLineEdit.text() and 
                    datadict[self.item.text()]["password"] == self.passwordLineEdit.text() and
                    datadict[self.item.text()]["website"] == self.websiteLineEdit.text())
            
        # if older registration does not has account 
        # then only need to check whether username, password, and website change
        else:
            return (datadict[self.item.text()]["username"] == self.usernameLineEdit.text() and 
                    datadict[self.item.text()]["password"] == self.passwordLineEdit.text() and
                    datadict[self.item.text()]["website"] == self.websiteLineEdit.text())
                
    def infoEmpty(self):
        """Return True if any information is empty"""
        if self.getAct() == "google" or self.getAct() == "wechat":
            return (" " in self.usernameLineEdit.text() or
                    " " in self.websiteLineEdit.text())
        else:
            return (" " in self.usernameLineEdit.text() or
                    " " in self.passwordLineEdit.text() or
                    " " in self.websiteLineEdit.text())