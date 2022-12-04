from PyQt5 import QtWidgets, QtGui, QtCore
from mainscreen import MainWindow
from registerwindow import RegisterWindow
from modifyRegisterWindow import ModifyRegisterWindow
from modify_register_ask_secrets import AskSecrets
from qtwidgets import PasswordEdit
import sys
import utils
import os
import json
import qdarktheme


class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        utils.set_style(self)
        self.initUI()
    

    def initUI(self):
        """Initialize window"""
        self.setWindowTitle("登录页面")
        self.setWindowIcon(QtGui.QIcon(utils.lock))
        
        # add menubar
        menu = QtWidgets.QMenu("主题", self)
        defaultTheme = QtWidgets.QAction("默认", self)
        kkTheme = QtWidgets.QAction("开开自定义", self)
        lightTheme = QtWidgets.QAction("浅色", self)
        darkTheme = QtWidgets.QAction("深色", self)
        
        menu.addAction(defaultTheme)
        menu.addAction(kkTheme)
        menu.addAction(lightTheme)
        menu.addAction(darkTheme)
        
        defaultTheme.triggered.connect(self.setDefaultTheme)
        kkTheme.triggered.connect(self.setkkTheme)
        lightTheme.triggered.connect(self.setLightTheme)
        darkTheme.triggered.connect(self.setDarkTheme)
        
        self.menuBar().addMenu(menu)
        
        # set layout
        widget = QtWidgets.QWidget()
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
        self.lineEdit_password = PasswordEdit()
        formlayout.addRow(self.password, self.lineEdit_password)
        
        # button layout
        buttonlayout = QtWidgets.QHBoxLayout()
        self.loginbutton = QtWidgets.QPushButton("登录")
        self.loginbutton.setMinimumSize(120, 70)
        self.loginbutton.clicked.connect(self.handleLogin)
        self.loginbutton.setStyleSheet(utils.pushbutton)
        
        self.registerbutton = QtWidgets.QPushButton("注册")
        self.registerbutton.setMinimumSize(120, 70)
        self.registerbutton.clicked.connect(self.handleRegister)
        self.registerbutton.setStyleSheet(utils.pushbutton)

        self.modifyRegistration = QtWidgets.QPushButton("修改/忘记密码")
        self.modifyRegistration.setMinimumSize(120, 70)
        self.modifyRegistration.clicked.connect(self.modifyRegister)
        self.modifyRegistration.setStyleSheet(utils.pushbutton)
        
        buttonlayout.addWidget(self.loginbutton)
        buttonlayout.addWidget(self.registerbutton)
        buttonlayout.addWidget(self.modifyRegistration)
        
        # set layout
        outerlayout.addLayout(formlayout)
        outerlayout.addLayout(buttonlayout)
        widget.setLayout(outerlayout)
        self.setCentralWidget(widget)
        

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
            self.window = MainWindow(self)
            self.window.show()
            self.hide()
        
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
            self.registerwindow = RegisterWindow(self)
            # utils.center(self.registerwindow)
            self.registerwindow.show()


    def modifyRegister(self):
        if not os.path.exists(utils.password_file):
            QtWidgets.QMessageBox.warning(self, '错误', '您还未注册')
        else:
            askSecrets = AskSecrets(self)
            askSecrets.show()
    
    
    def match_password(self):
        with open(utils.password_file, "r") as f:
            password = json.load(f)
        if (password['username'] == self.lineEdit_username.text() and
            password['password'] == self.lineEdit_password.text()):
            return True
        return False
    
    
    def setDefaultTheme(self):
        style = QtWidgets.QStyleFactory.create("Fusion")
        self.setStyle(style)
        stylesheet = open(utils.stylesheet, "w")
        stylesheet.write(
            """* {
                font-size: 18pt; 
                font-family: HanyiSentyMarshmallow; 
            }""")
        stylesheet.close()
        with open(utils.stylesheet) as f:
            self.setStyleSheet(f.read())
    
    
    def setkkTheme(self):
        style = QtWidgets.QStyleFactory.create("Fusion")
        self.setStyle(style)
        stylesheet = open(utils.stylesheet, "w")
        stylesheet.write(
            """* {
               font-size: 18pt; 
               font-family: HanyiSentyMarshmallow; 
               background-color: #cae9ff; 
            }""")
        stylesheet.close()
        with open(utils.stylesheet) as f:
            self.setStyleSheet(f.read())
        
        
    def setLightTheme(self):
        self.setStyleSheet(utils.style)
        stylesheet = open(utils.stylesheet, "w")
        stylesheet.write(qdarktheme.load_stylesheet("light"))
        stylesheet.close()
        stylesheet = open(utils.stylesheet, "a")
        stylesheet.write(
            """* {
                font-size: 18pt; 
                font-family: HanyiSentyMarshmallow;
            }""")
        stylesheet.close()
        with open(utils.stylesheet) as f:
            self.setStyleSheet(f.read())
    
    
    def setDarkTheme(self):
        self.setStyleSheet(utils.style)
        stylesheet = open(utils.stylesheet, "w")
        stylesheet.write(qdarktheme.load_stylesheet("dark"))
        stylesheet.close()
        stylesheet = open(utils.stylesheet, "a")
        stylesheet.write(
            """* {
                font-size: 18pt; 
                font-family: HanyiSentyMarshmallow;
            }""")
        stylesheet.close()
        with open(utils.stylesheet) as f:
            self.setStyleSheet(f.read())
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())

    