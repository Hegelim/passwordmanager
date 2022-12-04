# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainpage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from savewindow import SaveWindow
from loadwindow import LoadWindow
import os
import shutil
import utils


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # utils.set_style(self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("密码管理助手")
        self.setWindowIcon(QtGui.QIcon(utils.card_file_box))
        
        # set layout
        widget = QWidget()
        outerlayout = QtWidgets.QVBoxLayout()

        # title
        self.label = QLabel()
        self.label.setText("欢迎使用密码管理小助手!")
        outerlayout.addWidget(self.label)
        
        options = QLabel()
        options.setText("请选择以下选项")
        outerlayout.addWidget(options)
        
        # buttons
        buttonslayout = QtWidgets.QGridLayout()
        
        # "保存"部分
        self.saveButton = QPushButton()
        self.saveButton.setMinimumSize(150, 80)
        self.saveButton.setText("保存")
        self.saveButton.clicked.connect(self.save)

        # “读取”部分
        self.loadButton = QPushButton()
        self.loadButton.setMinimumSize(150, 80)
        self.loadButton.setText("读取")
        self.loadButton.clicked.connect(self.load)
        
        # “同步”部分
        self.syncButton = QPushButton()
        self.syncButton.setMinimumSize(150, 80)
        self.syncButton.setText("备份至云端")
        self.syncButton.clicked.connect(self.sync)
        
        # "导出"
        self.exportButton = QPushButton()
        self.exportButton.setMinimumSize(150, 80)
        self.exportButton.setText("导出")
        self.exportButton.clicked.connect(self.export)

        buttonslayout.addWidget(self.saveButton, 0, 0, 1, 2)
        buttonslayout.addWidget(self.loadButton, 0, 2, 1, 2)
        buttonslayout.addWidget(self.syncButton, 1, 0, 1, 2)
        buttonslayout.addWidget(self.exportButton, 1, 2, 1, 2)
        
        # nest layout
        outerlayout.addLayout(buttonslayout)
        widget.setLayout(outerlayout)
        self.setCentralWidget(widget)
        

    def save(self):
        self.savewindow = SaveWindow(self)
        self.savewindow.show()

    def load(self):
        self.loadwindow = LoadWindow(self)
        self.loadwindow.show()
        
    def sync(self):
        if os.path.exists("database.pkl"):
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
            drive = GoogleDrive(gauth)
            # Specify Google Drive folder id
            file = drive.CreateFile({'parents': [{'id': '1rGC92pX8lKrktQ0dJhuwKZ7V0NNCfjKw'}]})
            file.SetContentFile('database.pkl')
            file.Upload()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("备份到云端成功！")
            msg.setWindowTitle("备份成功")
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("错误")
            msg.setInformativeText("您还未保存任何密码")
            msg.setWindowTitle("错误")
            msg.exec()
            
    def export(self):
        if os.path.exists(utils.database_file):
            dir_name = QFileDialog.getExistingDirectory(self, "选择导出目录")
            # dir might not have been selected
            if dir_name:
                if os.path.exists(os.path.join(dir_name, utils.database_file)):
                    msg = QtWidgets.QMessageBox(self)
                    msg.setWindowTitle("导出")
                    msg.setIcon(QMessageBox.Question)
                    msg.setText(f"您要导出到{os.path.join(dir_name, utils.database_file)}")
                    msg.setInformativeText("文件已存在，继续吗？")
                    msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
                    msg.setDefaultButton(QMessageBox.Cancel)
                    if msg.exec() == QtWidgets.QMessageBox.Save:
                        shutil.copy(utils.database_file, os.path.join(dir_name, utils.database_file))
                        QtWidgets.QMessageBox.information(self, '成功', "导出成功")
                    else:
                        QtWidgets.QMessageBox.information(self, '取消', "已取消")
                    
                else:
                    msg = QtWidgets.QMessageBox(self)
                    msg.setWindowTitle("导出")
                    msg.setIcon(QMessageBox.Question)
                    msg.setText(f"您要导出到{os.path.join(dir_name, utils.database_file)}")
                    msg.setInformativeText("继续吗？")
                    msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
                    msg.setDefaultButton(QMessageBox.Cancel)
                    if msg.exec() == QtWidgets.QMessageBox.Save:
                        shutil.copy(utils.database_file, os.path.join(dir_name, utils.database_file))
                        QtWidgets.QMessageBox.information(self, '成功', "导出成功")
                    else:
                        QtWidgets.QMessageBox.information(self, '取消', "已取消")

        else:
            QtWidgets.QMessageBox.warning(self, '警告', "您还未保存任何密码")
