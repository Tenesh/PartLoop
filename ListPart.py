from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from PyQt5.uic import loadUiType

listpart_ui, _ = loadUiType('Ui/ListPartLoop.ui')


class ListPartApp(QDialog, listpart_ui):
    def __init__(self, parent=None):
        super(ListPartApp, self).__init__(parent)
        self.setupUi(self)