from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from Connect import ConnectDatabase
from PyQt5.uic import loadUiType

# Global Variable
addentry_ui, _ = loadUiType('Ui/AddEntryPartLoop.ui')


class AddEntryApp(QDialog, addentry_ui):
    def __init__(self, parent=None):
        super(AddEntryApp, self).__init__(parent)
        self.setupUi(self)
        self.ShowEmployee_custom()

    # Method to show drop-down data
    def ShowEmployee_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT employee_name FROM employee')
        employee_list = self.cur.fetchall()
        for employee in employee_list:
            self.comboBoxNewEntryEmployee.addItem(employee[0])
        self.db.close()

    def ShowName_part(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT part_name FROM part')
        part_list = self.cur.fetchall()
        for part in part_list:
            self.comboBoxNewEntry.addItem(part[0])
        self.db.close()
