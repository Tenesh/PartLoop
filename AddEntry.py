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
        self.ShowName_part()
        self.ShowStatus_entry()
        self.HandleButtonAction()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonNewEntryAdd.clicked.connect(self.AddEntry_validate)
        self.pushButtonNewEntryReset.clicked.connect(self.AddEntry_reset)

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
            self.comboBoxNewEntryPart.addItem(part[0])
        self.db.close()

    def ShowStatus_entry(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT status_name FROM status')
        status_list = self.cur.fetchall()
        for status in status_list:
            self.comboBoxNewEntryStatus.addItem(status[0])
        self.db.close()

    # Method to validate empty field data entry
    def AddEntry_validate(self):
        if not self.lineNewEntryDescription.toPlainText() == '':
            self.AddEntry_Data()
        else:
            self.error_popup("Input Error", "Invalid input or empty Description field")

    # Method to reset all add part fields
    def AddEntry_reset(self):
        self.comboBoxNewEntryPart.clear()
        self.comboBoxNewEntryEmployee.clear()
        self.comboBoxNewEntryStatus.clear()
        self.spinBoxNewEntryQuantity.clear()
        self.lineNewEntryDescription.clear()
        self.comboBoxNewEntryEmployee.clear()
        self.spinBoxNewEntryQuantity.setValue(1)
        self.ShowName_part()
        self.ShowEmployee_custom()
        self.ShowStatus_entry()

    # Method to add entry data
    def AddEntry_Data(self):
        self.db = ConnectDatabase()
        part_id = self.comboBoxNewEntryPart.currentText()
        entry_employee = self.comboBoxNewEntryEmployee.currentText()
        entry_status = self.comboBoxNewEntryStatus.currentText()
        entry_quantity = self.spinBoxNewEntryQuantity.value()
        entry_description = self.lineNewEntryDescription.toPlainText()
        entry_date = self.dateNewEntryDate.text()

        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            self.cur.execute('''INSERT INTO entry (part_id, entry_status, entry_qty, entry_desc, entry_date, entry_employee)
                                                    VALUES ((SELECT id FROM part WHERE part_name = %s) , %s , %s , %s , %s , %s)''', (part_id, entry_status, entry_quantity, entry_description, entry_date, entry_employee))
        except Exception as error:
            self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
            self.AddEntry_reset()
            self.error_popup("Input Error", error)
        else:
            self.cur.execute('RELEASE SAVEPOINT SP1')
            self.db.commit()
            self.AddEntry_reset()
            self.success_popup("Entry", "New Entry Added.")
        self.db.close()

    # Method to show success popup window
    def success_popup(self, title_popup, msg_popup):
        popup = QMessageBox()
        popup.setFixedSize(500, 500)
        popup.setWindowTitle(title_popup)
        popup.setIcon(QMessageBox.Information)
        popup.setStyleSheet("font:9pt Poppins;")
        popup.setText(msg_popup)
        popup.exec_()

    # Method to show error popup window
    def error_popup(self, title_popup, msg_popup):
        popup = QMessageBox()
        popup.setFixedSize(500, 500)
        popup.setWindowTitle(title_popup)
        popup.setIcon(QMessageBox.Warning)
        popup.setStyleSheet("font:9pt Poppins;")
        popup.setText(msg_popup)
        popup.exec_()