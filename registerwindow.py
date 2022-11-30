from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import utils
import json


class RegisterWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("注册")
        
        # add label
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("请输入以下信息")
        layout.addWidget(label)
        
        # add form
        formlayout = QtWidgets.QFormLayout()
        self.username_edit = QtWidgets.QLineEdit()
        self.password1_edit = QtWidgets.QLineEdit()
        self.password2_edit = QtWidgets.QLineEdit()
        formlayout.addRow("用户名：", self.username_edit)
        formlayout.addRow("密码：", self.password1_edit)
        formlayout.addRow("请再次输入密码", self.password2_edit)
        
        # add buttons
        buttonlayout = QtWidgets.QHBoxLayout()
        savebutton = QtWidgets.QPushButton("保存", self)
        savebutton.clicked.connect(self.handlesave)
        cancelbutton = QtWidgets.QPushButton("取消", self)
        cancelbutton.clicked.connect(self.handlecancel)
        buttonlayout.addWidget(savebutton)
        buttonlayout.addWidget(cancelbutton)
        
        # nest layouts
        layout.addLayout(formlayout)
        layout.addLayout(buttonlayout)
        self.setLayout(layout)
        utils.center(self)
        
        
    def handlesave(self):
        # if any field is empty
        if (self.username_edit.text() == "" or 
            self.password1_edit.text() == "" or 
            self.password2_edit.text() == ""):
            QtWidgets.QMessageBox.warning(self, '错误', '输入不能为空')
        
        # if 2 passwords don't match
        elif self.password1_edit.text() != self.password2_edit.text():
            QtWidgets.QMessageBox.warning(self, '错误', '两次密码输入不一致')

        # if any input contains whitespace
        elif (self.username_edit.text().isspace() or
              self.password1_edit.text().isspace() or
              self.password2_edit.text().isspace()):
            QtWidgets.QMessageBox.warning(self, '错误', '不能输入空格')
            
        # save password 
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText("保存密码确认")
            msg.setInformativeText("您确定要保存该信息吗？")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Save)
            if msg.exec_() == QMessageBox.Save:
                password = {}
                password["username"] = self.username_edit.text()
                password['password'] = self.password1_edit.text()
                with open(utils.password_file, "w") as f:
                    json.dump(password, f)
                QtWidgets.QMessageBox.information(self, '成功', '密码保存成功！')
                self.close()
    
    def handlecancel(self):
        self.close()