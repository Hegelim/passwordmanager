from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import os
import pickle
from updatewindow import UpdateWindow


class LoadWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python")
        self.setGeometry(500, 200, 300, 400)

        self.formGroupBox = QGroupBox("注册信息")
        self.nameLineEdit = QLineEdit()
        self.createForm()

        self.searchButton = QPushButton(self)
        self.searchButton.setText("搜索")
        self.searchButton.clicked.connect(self.search)

        # =============================
        self.listWidget = QListWidget(self)
        self.displayregistration()
        self.listWidget.itemDoubleClicked.connect(self.doubleClickInfo)

        # =============================
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.deleteButton = self.buttonBox.addButton("Delete", QDialogButtonBox.ActionRole)
        self.deleteButton.clicked.connect(self.deleteEntry)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # ==========================
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.searchButton)
        mainLayout.addWidget(self.listWidget)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def displayregistration(self):
        if os.path.exists("database.pkl"):
            with open("database.pkl", "rb") as f:
                datadict = pickle.load(f)

            for key in datadict.keys():
                QListWidgetItem(key, self.listWidget)

    def search(self):
        self.listWidget.clear()
        if os.path.exists("database.pkl"):
            with open("database.pkl", "rb") as f:
                datadict = pickle.load(f)

            if self.nameLineEdit.text() == "":
                for key in datadict.keys():
                    QListWidgetItem(key, self.listWidget)
            else:
                for key in datadict.keys():
                    if self.nameLineEdit.text().lower() in key.lower():
                        QListWidgetItem(key, self.listWidget)

    def doubleClickInfo(self, item):
        self.updatewindow = UpdateWindow(item)
        self.updatewindow.show()


    def deleteEntry(self):
        if os.path.exists("database.pkl"):
            if not self.listWidget.currentItem():
                QtWidgets.QMessageBox.warning(self, "错误", "您还未选取任何记录")
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("删除")
                msg.setIcon(QMessageBox.Question)
                msg.setText(f"您要删除{self.listWidget.currentItem().text()}")
                msg.setInformativeText("继续吗？")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                msg.setDefaultButton(QMessageBox.Cancel)
                if msg.exec() == QMessageBox.Yes:
                    with open("database.pkl", "rb") as f:
                        datadict = pickle.load(f)

                    datadict.pop(self.listWidget.currentItem().text())

                    self.listWidget.clear()
                    for key in datadict.keys():
                        QListWidgetItem(key, self.listWidget)

                    with open('database.pkl', 'wb') as f:
                        pickle.dump(datadict, f)
                    QtWidgets.QMessageBox.information(self, "删除", "删除成功")


    def createForm(self):
        # creating a form layout
        layout = QFormLayout()
        layout.addRow(QLabel("名称"), self.nameLineEdit)
        self.formGroupBox.setLayout(layout)
