from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from Connect import ConnectDatabase
from PyQt5.uic import loadUiType

# Global Variable
addpart_ui, _ = loadUiType('Ui/AddPartLoop.ui')


class AddPartApp(QDialog, addpart_ui):
    def __init__(self, parent=None):
        super(AddPartApp, self).__init__(parent)
        self.setupUi(self)
        self.ShowDepartment_custom()
        self.ShowStorage_custom()
        self.ShowCategory_custom()

    # Method to show drop-down data
    def ShowDepartment_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT department_name FROM department')
        department_list = self.cur.fetchall()
        for department in department_list:
            self.comboBoxNewPartDepartment.addItem(department[0])
        self.db.close()

    def ShowCategory_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT category_name FROM category')
        category_list = self.cur.fetchall()
        for category in category_list:
            self.comboBoxNewPartCategory.addItem(category[0])
        self.db.close()

    def ShowStorage_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT storage_name FROM storage')
        storage_list = self.cur.fetchall()
        for storage in storage_list:
            self.comboBoxNewPartStorage.addItem(storage[0])
        self.db.close()