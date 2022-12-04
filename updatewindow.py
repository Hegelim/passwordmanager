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
        self.formGroupBox = QGroupBox("注册信息")
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
        if os.path.exists(utils.database_file):
            with open(utils.database_file, "rb") as f:
                datadict = pickle.load(f)
            
            # 1. if the information doesn't change
            if (datadict[self.item.text()]["username"] == self.usernameLineEdit.text() and 
                datadict[self.item.text()]["password"] == self.passwordLineEdit.text() and
                datadict[self.item.text()]["website"] == self.websiteLineEdit.text()):
                QtWidgets.QMessageBox.warning(self, "更改", "您未做任何更改")
                
                
            # 2. if any input is empty
            elif (self.usernameLineEdit.text() == "" or
                  self.passwordLineEdit.text() == "" or
                  self.websiteLineEdit.text() == ""):
                QtWidgets.QMessageBox.warning(self, "更改", "输入不能为空")
                
            # 3. the user does update the information
            else:
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("更改")
                msg.setIcon(QMessageBox.Question)
                msg.setText(f"您要更新该信息")
                msg.setInformativeText("继续吗？")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                if msg.exec() == QMessageBox.Yes:
                    datadict[self.item.text()]["username"] = self.usernameLineEdit.text()
                    datadict[self.item.text()]["password"] = self.passwordLineEdit.text()
                    datadict[self.item.text()]["website"] = self.websiteLineEdit.text()

                    with open(utils.database_file, "wb") as f:
                        pickle.dump(datadict, f)
                    
                    QtWidgets.QMessageBox.warning(self, "更改", "更改成功！")
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, "更改", "已取消更改")


    def createForm(self, item):
        layout = QFormLayout()
        layout.addRow(QLabel("用户名:"), self.usernameLineEdit)
        layout.addRow(QLabel("密码:"), self.passwordLineEdit)
        layout.addRow(QLabel("网址:"), self.websiteLineEdit)

        if os.path.exists(utils.database_file):
            with open(utils.database_file, "rb") as f:
                datadict = pickle.load(f)

            self.usernameLineEdit.setText(datadict[item.text()]["username"])
            self.passwordLineEdit.setText(datadict[item.text()]["password"])
            self.websiteLineEdit.setText(datadict[item.text()]["website"])

        self.formGroupBox.setLayout(layout)
