from PyQt5 import QtWidgets, QtGui, QtCore
from mainscreen import MainWindow
from registerwindow import RegisterWindow
from qtwidgets import PasswordEdit
import sys
import utils
import os
import json
import qdarktheme

# global variable theme
THEME = ""


class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        utils.set_style(self)
        self.initUI()
    

    def initUI(self):
        """Initialize window"""
        self.setWindowTitle("登录页面")
        self.setWindowIcon(QtGui.QIcon(utils.lock))
        utils.center(self)
        
        # add menubar
        menu = QtWidgets.QMenu("菜单", self)
        defaultTheme = QtWidgets.QAction("默认主题", self)
        kkTheme = QtWidgets.QAction("开开自定义主题", self)
        lightTheme = QtWidgets.QAction("Light", self)
        darkTheme = QtWidgets.QAction("Dark", self)
        
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
        
        # self.lineEdit_password = QtWidgets.QLineEdit()
        # self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        # formlayout.addRow(self.password, self.lineEdit_password)
        self.lineEdit_password = PasswordEdit()
        formlayout.addRow(self.password, self.lineEdit_password)

        
        # button layout
        buttonlayout = QtWidgets.QHBoxLayout()
        self.loginbutton = QtWidgets.QPushButton("登录")
        self.loginbutton.setMinimumSize(80, 50)
        self.loginbutton.clicked.connect(self.handleLogin)
        self.loginbutton.setStyleSheet(utils.pushbutton)
        
        self.registerbutton = QtWidgets.QPushButton("注册")
        self.registerbutton.setMinimumSize(80, 50)
        self.registerbutton.clicked.connect(self.handleRegister)
        self.registerbutton.setStyleSheet(utils.pushbutton)

        
        self.forgetbutton = QtWidgets.QPushButton("忘记密码")
        self.forgetbutton.setMinimumSize(80, 50)
        self.forgetbutton.clicked.connect(self.handleForget)
        self.forgetbutton.setStyleSheet(utils.pushbutton)
        buttonlayout.addWidget(self.loginbutton)
        buttonlayout.addWidget(self.registerbutton)
        buttonlayout.addWidget(self.forgetbutton)
        
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
        

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # if THEME == "kktheme":
    #     app.setStyle("Fusion")
    #     app.setStyleSheet(utils.style)
    # elif THEME == "fusion":
    #     app.setStyle("Fusion")
    # stylesheet = qdarktheme.load_stylesheet(custom_colors={
    #             "background": '#cae9ff', 
    #             })
    # app.setStyleSheet(stylesheet)
    login = Login()
    login.show()
    sys.exit(app.exec_())

    