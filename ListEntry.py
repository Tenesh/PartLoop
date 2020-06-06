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
        self.ClearDropDown()
        self.ListEntry_show()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonListEntrySearch.clicked.connect(self.ListEntry_show)
        self.pushButtonListEntryReset.clicked.connect(self.ListEntry_reset)

    # Method to set empty value in drop-down field
    def ClearDropDown(self):
        self.comboBoxListEntryDepartment.setCurrentText('')
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
        field_status = self.comboBoxListEntryStatus.currentText()
        search_name = '%{}%'.format(field_name)
        search_department = '%{}%'.format(field_department)
        search_status = '%{}%'.format(field_status)
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        try:
            self.cur.execute('''SELECT entry.id, entry.entry_date, part.part_name, part.part_department, 
            entry.entry_status, entry.entry_qty, entry.entry_employee, entry.entry_desc FROM entry JOIN part ON 
            entry.part_id = part.id WHERE part.part_name ILIKE %s AND part.part_department ILIKE %s AND 
            entry.entry_status ILIKE %s ORDER BY entry.id ASC''',
                             (search_name, search_department, search_status))
            fetch_data = self.cur.fetchall()
        except Exception as error:
            self.error_popup("Duplicate Error", "Failed to connect database")
        else:
            if fetch_data is None:
                self.tableWidgetListEntry.setRowCount(0)
                self.error_popup("List Entry", "No records found!")
            else:
                self.tableWidgetListEntry.setRowCount(0)
                self.tableWidgetListEntry.insertRow(0)
                for row, form in enumerate(fetch_data):
                    for column, item in enumerate(form):
                        self.tableWidgetListEntry.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1
                        row_position = self.tableWidgetListEntry.rowCount()
                        self.tableWidgetListEntry.insertRow(row_position)
                        self.tableWidgetListEntry.resizeColumnsToContents()
        self.db.close()

    # Method to reset list of entry
    def ListEntry_reset(self):
        self.ClearDropDown()
        self.lineListEntryPartName.clear()
        self.ListEntry_show()

    # Method to show error popup window
    def error_popup(self, title_popup, msg_popup):
        popup = QMessageBox()
        popup.setFixedSize(500, 500)
        popup.setWindowTitle(title_popup)
        popup.setIcon(QMessageBox.Warning)
        popup.setStyleSheet("font:9pt Poppins;")
        popup.setText(msg_popup)
        popup.exec_()