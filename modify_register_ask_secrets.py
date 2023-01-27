from PyQt5 import QtWidgets, QtGui
import utils
import json
from qtwidgets import PasswordEdit
from modifyRegisterWindow import ModifyRegisterWindow


class AskSecrets(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle("更新注册")
        
        # initiate layout
        outerlayout = QtWidgets.QVBoxLayout()
        formlayout = QtWidgets.QFormLayout()
        self.secrets = PasswordEdit()
        formlayout.addRow("请输入找回密钥", self.secrets)
        
        # add 2 buttons
        buttons = QtWidgets.QDialogButtonBox(self)
        confirmButton = buttons.addButton("确认", QtWidgets.QDialogButtonBox.ActionRole)
        cancelButton = buttons.addButton("取消", QtWidgets.QDialogButtonBox.RejectRole)
        
        # link to functions
        confirmButton.clicked.connect(self.check_secrets)
        cancelButton.clicked.connect(lambda: self.close())
        
        # add layout
        outerlayout.addLayout(formlayout)
        outerlayout.addWidget(buttons)
        self.setLayout(outerlayout)
            
        
    def check_secrets(self):
        with open(utils.password_file, "r") as f:
            password = json.load(f)
        
        # if empty
        if utils.isInvalidText(self.secrets.text()):
            QtWidgets.QMessageBox.warning(self, "错误", "输入不能为空或含有空格")
        # if secrets is not 6 digit number
        elif not (self.secrets.text().isdigit() and len(self.secrets.text()) == 6):
            QtWidgets.QMessageBox.warning(self, "错误", "请输入6位数字")
        # if secrets don't match secrets
        elif password['secrets'] != self.secrets.text():
            QtWidgets.QMessageBox.warning(self, "错误", "输入有误")
        # if secrets match
        else:
            modifyWindow = ModifyRegisterWindow(self)
            modifyWindow.show()
            self.close()
