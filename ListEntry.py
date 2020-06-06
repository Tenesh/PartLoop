from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from PyQt5.uic import loadUiType
from Connect import ConnectDatabase

# Global Variable
listentry_ui, _ = loadUiType('Ui/ListEntryPartLoop.ui')


class ListEntryApp(QDialog, listentry_ui):
    def __init__(self, parent=None):
        super(ListEntryApp, self).__init__(parent)
        self.setupUi(self)
        self.HandleButtonAction()
        self.ShowDepartment_custom()
        self.ShowStatus_entry()
        self.ShowStorage_custom()
        self.ShowCategory_custom()
        self.ClearDropDown()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonListEntrySearch.clicked.connect(self.ListEntry_show)
        self.pushButtonListEntryReset.clicked.connect(self.ListEntry_reset)

    # Method to set empty value in drop-down field
    def ClearDropDown(self):
        self.comboBoxListEntryDepartment.setCurrentText('')
        self.comboBoxListEntryCategory.setCurrentText('')
        self.comboBoxListEntryStorage.setCurrentText('')
        self.comboBoxListEntryStatus.setCurrentText('')

    # Method to show drop-down data
    def ShowDepartment_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT department_name FROM department ORDER BY department_name ASC')
        department_list = self.cur.fetchall()
        for department in department_list:
            self.comboBoxListEntryDepartment.addItem(department[0])
        self.db.close()

    def ShowCategory_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT category_name FROM category ORDER BY category_name ASC')
        category_list = self.cur.fetchall()
        for category in category_list:
            self.comboBoxListEntryCategory.addItem(category[0])
        self.db.close()

    def ShowStorage_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT storage_name FROM storage ORDER BY storage_name ASC')
        storage_list = self.cur.fetchall()
        for storage in storage_list:
            self.comboBoxListEntryStorage.addItem(storage[0])
        self.db.close()

    def ShowStatus_entry(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT status_name FROM status ORDER BY status_name ASC')
        status_list = self.cur.fetchall()
        for status in status_list:
            self.comboBoxListEntryStatus.addItem(status[0])
        self.db.close()

    # Method to show list of entry
    def ListEntry_show(self):
        field_name = self.lineListEntryPartName.text()
        field_department = self.comboBoxListEntryDepartment.currentText()
        field_category = self.comboBoxListEntryCategory.currentText()
        field_storage = self.comboBoxListEntryStorage.currentText()
        field_status = self.comboBoxListEntryStatus.currentText()
        search_name = '%{}%'.format(field_name)
        search_department = '%{}%'.format(field_department)
        search_category = '%{}%'.format(field_category)
        search_storage = '%{}%'.format(field_storage)
        search_status = '%{}%'.format(field_status)
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()

        try:
            self.cur.execute('''SELECT entry.id, part.part_name, part.part_department, part.part_category, 
            part.part_storage, entry.entry_status, entry.entry_qty, entry.entry_desc, entry.entry_date, 
            entry.entry_employee FROM entry JOIN part ON entry.part_id = part.id WHERE part.part_name ILIKE %s AND 
            part.part_department ILIKE %s AND part.part_category ILIKE %s AND part.part_storage ILIKE %s AND 
            entry.entry_status ILIKE %s''', (search_name, search_department, search_category, search_storage,
                                             search_status))
            fetch_data = self.cur.fetchall()
        except Exception as error:
            print(str(error))
        else:
            for data in fetch_data:
                print(data)

    # Method to reset list of entry
    def ListEntry_reset(self):
        pass
