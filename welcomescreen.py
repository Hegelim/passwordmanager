from PyQt5 import QtWidgets, QtGui
from mainscreen import MainWindow
from registerwindow import RegisterWindow
from modify_register_ask_secrets import AskSecrets
from qtwidgets import PasswordEdit
import sys
import utils
import os
import json
import qdarktheme
import time
import pyotp
import qrcode
import base64


class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        utils.set_style(self)
        self.initUI()
    

    def initUI(self):
        """Initialize window"""
        self.setWindowTitle("登录页面")
        self.setWindowIcon(QtGui.QIcon(utils.lock))
        
        # add Theme Menu
        themeMenu = QtWidgets.QMenu("&主题", self)
        
        defaultTheme = QtWidgets.QAction("默认", self)
        kkTheme = QtWidgets.QAction("开开自定义", self)
        lightTheme = QtWidgets.QAction("浅色", self)
        darkTheme = QtWidgets.QAction("深色", self)
        
        themeMenu.addAction(defaultTheme)
        themeMenu.addAction(kkTheme)
        themeMenu.addAction(lightTheme)
        themeMenu.addAction(darkTheme)
        
        defaultTheme.triggered.connect(self.setDefaultTheme)
        kkTheme.triggered.connect(self.setkkTheme)
        lightTheme.triggered.connect(self.setLightTheme)
        darkTheme.triggered.connect(self.setDarkTheme)
        
        self.menuBar().addMenu(themeMenu)
        
        # add Help Menu
        helpMenu = self.menuBar().addMenu("&帮助")
        helpAction = QtWidgets.QAction("安装信息", self)
        helpAction.triggered.connect(self.showInfo)
        helpMenu.addAction(helpAction)
        
        # add Login Menu
        loginMenu = self.menuBar().addMenu("&登录")
        passwordLogin = QtWidgets.QAction("账号密码登录", self)
        passwordLogin.triggered.connect(self.passwordLoginLayout)
        qrcodeLogin = QtWidgets.QAction("手机扫码登录", self)
        qrcodeLogin.triggered.connect(self.qrcodeLoginLayout)
        loginMenu.addAction(passwordLogin)
        loginMenu.addAction(qrcodeLogin)
        # by default, use password login
        passwordLogin.trigger()

    def passwordLoginLayout(self):
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
        self.loginbutton.setMinimumSize(100, 70)
        self.loginbutton.clicked.connect(self.handleLogin)
        self.loginbutton.setStyleSheet(utils.pushbutton)
        
        self.registerbutton = QtWidgets.QPushButton("注册")
        self.registerbutton.setMinimumSize(100, 70)
        self.registerbutton.clicked.connect(self.handleRegister)
        self.registerbutton.setStyleSheet(utils.pushbutton)

        self.modifyRegistration = QtWidgets.QPushButton("修改/忘记密码")
        self.modifyRegistration.setMinimumSize(160, 70)
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


    def qrcodeLoginLayout(self):
        # create widget
        widget = QtWidgets.QWidget()
        
        # create outer layout
        outerLayout = QtWidgets.QVBoxLayout()
        
        
        ## add lable ##
        outerLayout.addWidget(QtWidgets.QLabel("请用手机扫描下方二维码"))
        
        ## add qrcode ##
        
        # have to use base32 secret
        # self.k = pyotp.random_base32()
        self.k = base64.b32encode("IamTheBest@2023".encode("ascii"))
        # generate URI
        totp_auth = pyotp.totp.TOTP(self.k).provisioning_uri(name='Hegelim', issuer_name='PasswordManager')
        # convert to QRCode
        qrcode.make(totp_auth).save("qr_auth.png")
        # display QRCode
        qrlabel = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("qr_auth.png")
        # adding image to label
        qrlabel.setPixmap(self.pixmap)
        outerLayout.addWidget(qrlabel)
    
        ## add form ##
        verifyForm = QtWidgets.QFormLayout()
        self.qrPassword = PasswordEdit()
        verifyForm.addRow(QtWidgets.QLabel("请输入手机上6位密码"), self.qrPassword)
        
        outerLayout.addLayout(verifyForm)
        
        ## add login button ##
        self.loginbutton = QtWidgets.QPushButton("登录")
        self.loginbutton.clicked.connect(self.qrLogin)
        self.loginbutton.setStyleSheet(utils.pushbutton)
        outerLayout.addWidget(self.loginbutton)            
            
        # set layout
        widget.setLayout(outerLayout)    
        self.setCentralWidget(widget)
        
        
    def qrLogin(self):
        totp = pyotp.TOTP(self.k)
        if totp.verify(int(self.qrPassword.text())):
            self.window = MainWindow()
            self.window.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, '错误', '密码错误')
        


    def handleLogin(self):
        # 1. check whether the user has registered
        if not os.path.exists(utils.password_file):
            QtWidgets.QMessageBox.warning(self, '错误', '您还未注册')
            
        # 2. check whether input is empty
        elif (utils.isInvalidText(self.lineEdit_username.text()) or 
              utils.isInvalidText(self.lineEdit_password.text())):
            QtWidgets.QMessageBox.warning(self, '错误', '输入不能为空或含有空格')
            
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
            self.registerwindow = RegisterWindow(self)
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
                font-family: Microsoft YaHei; 
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
               font-family: Microsoft YaHei; 
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
                font-family: Microsoft YaHei;
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
                font-family: Microsoft YaHei;
            }""")
        stylesheet.close()
        with open(utils.stylesheet) as f:
            self.setStyleSheet(f.read())
            
            
    def showInfo(self):
        diagbox = QtWidgets.QDialog(self)
        diagbox.setWindowTitle("安装信息")
        
        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(f"安装目录: {os.getcwd()}"))
        layout.addWidget(QtWidgets.QLabel(f"版本信息: v1.2.0"))
        layout.addWidget(QtWidgets.QLabel(f"发布时间: 2023.1.22"))
        layout.addWidget(QtWidgets.QLabel(f"联系开发者: yz4175@columbia.edu"))
        buttonBox = QtWidgets.QDialogButtonBox(self)
        okbutton = buttonBox.addButton("好的", QtWidgets.QDialogButtonBox.AcceptRole)
        okbutton.clicked.connect(diagbox.accept)
        layout.addWidget(buttonBox)
        diagbox.setLayout(layout)
        diagbox.exec()
        
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())

    