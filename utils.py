"""Provide utility functions"""
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDesktopWidget


# this is used to save the password 
# using keyring
service_id = "password_manager"

# password file
password_file = "password.json"

# database
database_file = "database.pkl"

# favicons
card_file_box = "favicons/card_file_box.png"
pen = "favicons/pen.png"
lock = "favicons/lock.png"


def center(window):
    """Move window to the center of the screen"""
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())


def gen_font(size, style="Microsoft YaHei"):
    """Generate Font"""
    return QtGui.QFont(style, size)


def set_button_min_size(btn, minw, minh):
    btn.setMinimumSize(minw, minh)