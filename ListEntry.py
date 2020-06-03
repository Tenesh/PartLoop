from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from PyQt5.uic import loadUiType

listentry_ui, _ = loadUiType('Ui/ListEntryPartLoop.ui')


class ListEntryApp(QDialog, listentry_ui):
    def __init__(self, parent=None):
        super(ListEntryApp, self).__init__(parent)
        self.setupUi(self)