"""Provide utility functions"""
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDesktopWidget
import os 

# this is used to save the password 
# using keyring
service_id = "password_manager"

# password file
password_file = "password.json"

# database
database_file = "database.pkl"

# favicons
card_file_box = os.path.abspath("favicons/card_file_box.png")
pen = os.path.abspath("favicons/pen.png")
lock = os.path.abspath("favicons/lock.png")

# color
color = "#cbf3f0"

# style sheet
style = """
font-size: 18pt; 
font-family: HanyiSentyMarshmallow; 
background-color: #cae9ff;
"""

pushbutton = """
QPushButton {
    padding: 10px;
}
"""
# border: 2px solid;
# border-radius: 20px;


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