"""读取界面"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtGui
import os
import pickle
from updatewindow import UpdateWindow
import utils


class LoadWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("读取")
        self.setWindowIcon(QtGui.QIcon(utils.card_file_box))

        self.formGroupBox = QGroupBox()
        # self.formGroupBox.setStyleSheet(
        #     """QGroupBox {
        #         padding-top: 30px;
        #     }
        #     """
        # )
        self.nameLineEdit = QLineEdit()
        formlayout = QtWidgets.QFormLayout()
        formlayout.addRow(QLabel("名称"), self.nameLineEdit)
        self.formGroupBox.setLayout(formlayout)

        self.searchButton = QPushButton(self)
        self.searchButton.setText("搜索")
        self.searchButton.clicked.connect(self.search)
        
        # =============================
        self.listWidget = QListWidget(self)
        self.listWidget.setMinimumHeight(400)
        self.listWidget.setMinimumWidth(400)
        self.displayregistration()
        self.listWidget.itemDoubleClicked.connect(self.doubleClickInfo)

        # =============================
        self.buttonBox = QDialogButtonBox(self)
        
        self.sortButton = self.buttonBox.addButton("排序", QDialogButtonBox.ActionRole)
        self.sortButton.clicked.connect(self.sortEntries)
        
        self.deleteButton = self.buttonBox.addButton("删除", QDialogButtonBox.ActionRole)
        self.deleteButton.clicked.connect(self.deleteEntry)
        
        self.closeButton = self.buttonBox.addButton("保存并返回", QDialogButtonBox.RejectRole)
        self.closeButton.clicked.connect(self.reject)

        # ==========================
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.searchButton)
        mainLayout.addWidget(self.listWidget)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)


    def displayregistration(self):
        if os.path.exists(utils.database_file):
            with open(utils.database_file, "rb") as f:
                datadict = pickle.load(f)

            for key in datadict.keys():
                QListWidgetItem(key, self.listWidget)


    def search(self):
        self.listWidget.clear()
        if os.path.exists(utils.database_file):
            with open(utils.database_file, "rb") as f:
                datadict = pickle.load(f)

            # if use didn't put anything for keyword
            # then display everything
            if self.nameLineEdit.text() == "":
                for key in datadict.keys():
                    QListWidgetItem(key, self.listWidget)
            else:
                for key in datadict.keys():
                    if self.nameLineEdit.text().lower() in key.lower():
                        QListWidgetItem(key, self.listWidget)
        else:
            QtWidgets.QMessageBox.information(self, "错误", "您还未存储任何记录")


    def sortEntries(self):
        self.listWidget.clear()
        sortedEntries = {}
        if os.path.exists(utils.database_file):
            with open(utils.database_file, "rb") as f:
                datadict = pickle.load(f)
                
            for key in sorted(datadict.keys(), key=lambda x: x.upper()):
                sortedEntries[key] = datadict[key]
                QListWidgetItem(key, self.listWidget)
            
            with open(utils.database_file, "wb") as f:
                pickle.dump(sortedEntries, f)
                
            QtWidgets.QMessageBox.information(self, "成功", "排序成功")
        else:
            QtWidgets.QMessageBox.information(self, "错误", "您还未存储任何记录")


    def doubleClickInfo(self, item):
        self.updatewindow = UpdateWindow(self, item)
        self.updatewindow.show()


    def deleteEntry(self):
        if os.path.exists(utils.database_file):
            if not self.listWidget.currentItem():
                QtWidgets.QMessageBox.warning(self, "错误", "您还未选取任何记录")
            else:
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("删除")
                msg.setIcon(QMessageBox.Question)
                msg.setText(f"您要删除{self.listWidget.currentItem().text()}")
                msg.setInformativeText("继续吗？")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                msg.setDefaultButton(QMessageBox.Cancel)
                if msg.exec() == QMessageBox.Yes:
                    with open(utils.database_file, "rb") as f:
                        datadict = pickle.load(f)

                    datadict.pop(self.listWidget.currentItem().text())

                    self.listWidget.clear()
                    for key in datadict.keys():
                        QListWidgetItem(key, self.listWidget)

                    with open(utils.database_file, 'wb') as f:
                        pickle.dump(datadict, f)
                    QtWidgets.QMessageBox.information(self, "删除", "删除成功")
