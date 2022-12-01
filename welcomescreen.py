from PyQt5 import QtWidgets, QtGui, QtCore
from mainscreen import MainWindow
from registerwindow import RegisterWindow
import sys
import utils
import os
import json


class Login(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('font-size: 15pt; font-family: Microsoft YaHei;')
        self.initUI()
    

    def initUI(self):
        """Initialize window"""
        self.setWindowTitle("登录页面")
        self.setWindowIcon(QtGui.QIcon(utils.lock))
        utils.center(self)
        
        # set layout
        outerlayout = QtWidgets.QVBoxLayout()
        
        # set label
        self.label = QtWidgets.QLabel("欢迎使用密码管理小助手")
        outerlayout.addWidget(self.label)
        
        # form
        formlayout = QtWidgets.QFormLayout()
        self.username = QtWidgets.QLabel("用户名")
        self.lineEdit_username = QtWidgets.QLineEdit()
        formlayout.addRow(self.username, self.lineEdit_username)
                
        self.password = QtWidgets.QLabel("密码")
        
        self.lineEdit_password = QtWidgets.QLineEdit()
        formlayout.addRow(self.password, self.lineEdit_password)
        
        # button layout
        buttonlayout = QtWidgets.QHBoxLayout()
        self.loginbutton = QtWidgets.QPushButton("登录")
        self.loginbutton.clicked.connect(self.handleLogin)
        
        self.registerbutton = QtWidgets.QPushButton("注册")
        self.registerbutton.clicked.connect(self.handleRegister)
        
        self.forgetbutton = QtWidgets.QPushButton("忘记密码")
        self.forgetbutton.clicked.connect(self.handleForget)
        buttonlayout.addWidget(self.loginbutton)
        buttonlayout.addWidget(self.registerbutton)
        buttonlayout.addWidget(self.forgetbutton)
        
        # set layout
        outerlayout.addLayout(formlayout)
        outerlayout.addLayout(buttonlayout)
        self.setLayout(outerlayout)


    def handleLogin(self):
        # 1. check whether the user has registered
        if not os.path.exists(utils.password_file):
            QtWidgets.QMessageBox.warning(self, '错误', '您还未注册')
            
        # 2. check whether input is empty
        elif (self.lineEdit_username.text() == "" or 
              self.lineEdit_password.text() == ""):
            QtWidgets.QMessageBox.warning(self, '错误', '输入不能为空')
            
        # 3. check whether it matches the password
        elif self.match_password():
            self.window = MainWindow()
            self.window.show()
            self.close()
        
        # 4. wrong password
        else:
            QtWidgets.QMessageBox.warning(self, '错误', '密码错误')


    def handleRegister(self):
        """Register password"""
        # first, check whether there already
        # exists registration information
        if os.path.exists(utils.password_file):
            QtWidgets.QMessageBox.warning(self, '错误', '您已注册')
        
        else:
            self.registerwindow = RegisterWindow()
            utils.center(self.registerwindow)
            self.registerwindow.show()


    def handleForget(self):
        QtWidgets.QMessageBox.information(self, '忘记密码', "请联系开发者并支付10元")
        
    
    def match_password(self):
        with open(utils.password_file, "r") as f:
            password = json.load(f)
        if (password['username'] == self.lineEdit_username.text() and
            password['password'] == self.lineEdit_password.text()):
            return True
        return False
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())

    