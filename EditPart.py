from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from PyQt5.uic import loadUiType

editpart_ui, _ = loadUiType('Ui/EditPartLoop.ui')

class EditPartApp(QDialog, editpart_ui):
    def __init__(self, parent=None):
        super(EditPartApp, self).__init__(parent)
        self.setupUi(self)