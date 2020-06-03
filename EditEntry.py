from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from PyQt5.uic import loadUiType

editentry_ui, _ = loadUiType('Ui/EditEntryPartLoop.ui')


class EditEntryApp(QDialog, editentry_ui):
    def __init__(self, parent=None):
        super(EditEntryApp, self).__init__(parent)
        self.setupUi(self)