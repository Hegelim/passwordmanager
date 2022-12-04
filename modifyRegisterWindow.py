from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from qtwidgets import PasswordEdit
import utils
import json


class ModifyRegisterWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle("修改注册")
        self.setWindowIcon(QtGui.QIcon(utils.pen))
        
        layout = QtWidgets.QVBoxLayout()
        
        # add form
        groupbox = QtWidgets.QGroupBox(self)
        
        with open(utils.password_file, "r") as f:
            password = json.load(f)
        
        formlayout = QtWidgets.QFormLayout()
        self.username_edit = QtWidgets.QLineEdit(password['username'])
        self.password1_edit = PasswordEdit()
        self.password2_edit = PasswordEdit()
        
        self.secrets = PasswordEdit()
        formlayout.addRow("用户名", self.username_edit)
        formlayout.addRow("密码", self.password1_edit)
        formlayout.addRow("请再次输入密码", self.password2_edit)
        formlayout.addRow("请输入6位数字用于找回密码", self.secrets)
        groupbox.setLayout(formlayout)
        
        # add buttons
        buttons = QtWidgets.QDialogButtonBox(self)
        saveButton = buttons.addButton("保存", QtWidgets.QDialogButtonBox.ActionRole)
        cancelButton = buttons.addButton("取消", QtWidgets.QDialogButtonBox.RejectRole)
        
        # link buttons to functions
        saveButton.clicked.connect(self.handlesave)
        cancelButton.clicked.connect(self.handlecancel)
        
        # nest layouts
        layout.addWidget(groupbox)
        layout.addWidget(buttons)        
        self.setLayout(layout)
        
        
    def handlesave(self):
        # if any field is empty
        if (self.username_edit.text() == "" or 
            self.password1_edit.text() == "" or 
            self.password2_edit.text() == "" or
            self.secrets.text() == ""):
            QtWidgets.QMessageBox.warning(self, '错误', '输入不能为空')
        
        # if 2 passwords don't match
        elif self.password1_edit.text() != self.password2_edit.text():
            QtWidgets.QMessageBox.warning(self, '错误', '两次密码输入不一致')

        # if any input contains whitespace
        elif (self.username_edit.text().isspace() or
              self.password1_edit.text().isspace() or
              self.password2_edit.text().isspace() or
              self.secrets.text().isspace()):
            QtWidgets.QMessageBox.warning(self, '错误', '不能输入空格')
            
        # if secrets is not 6-digit number
        elif not (self.secrets.text().isdigit() and len(self.secrets.text()) == 6):
            QtWidgets.QMessageBox.warning(self, '错误', '请输入6位数字')
            
        # save password 
        else:
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle("保存")
            msg.setText("保存密码确认")
            msg.setInformativeText("您确定要保存该信息吗？")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Save)
            if msg.exec_() == QMessageBox.Save:
                password = {}
                password["username"] = self.username_edit.text()
                password['password'] = self.password1_edit.text()
                password['secrets'] = self.secrets.text()
                with open(utils.password_file, "w") as f:
                    json.dump(password, f)
                QtWidgets.QMessageBox.information(self, '成功', '账号保存成功！')
                self.close()
    
    def handlecancel(self):
        self.close()