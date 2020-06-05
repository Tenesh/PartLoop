from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from Connect import ConnectDatabase
from PyQt5.uic import loadUiType
from psycopg2 import IntegrityError

# Global Variable
editentry_ui, _ = loadUiType('Ui/EditEntryPartLoop.ui')


class EditEntryApp(QDialog, editentry_ui):
    def __init__(self, entry_id, parent=None):
        super(EditEntryApp, self).__init__(parent)
        self.setupUi(self)
        self.ShowEmployee_custom()
        self.ShowStatus_entry()
        self.HandleButtonAction()
        self.EditEntry_search(entry_id)
        self.lineEditEntryId.setText(str(entry_id))

    # Method to show drop-down data
    def ShowEmployee_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT employee_name FROM employee')
        employee_list = self.cur.fetchall()
        for employee in employee_list:
            self.comboBoxEditEntryEmployee.addItem(employee[0])
        self.db.close()

    def ShowStatus_entry(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT status_name FROM status')
        status_list = self.cur.fetchall()
        for status in status_list:
            self.comboBoxEditEntryStatus.addItem(status[0])
        self.db.close()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonEditEntrySave.clicked.connect(self.save_action)
        self.pushButtonEditEntryUndo.clicked.connect(self.EditEntry_undo)
        self.pushButtonEditEntryDelete.clicked.connect(self.delete_action)

    # Method to search the entry
    def EditEntry_search(self, entry_id):
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('''SELECT entry.id, part.part_name, entry.entry_status, entry.entry_qty, 
            entry.entry_desc, entry.entry_date, entry.entry_employee FROM entry JOIN part ON entry.part_id = part.id 
            WHERE entry.id = %s''', [(entry_id,)])
            fetch_data = self.cur.fetchone()
            print(fetch_data)
            print(len(fetch_data[2]))
            self.lineEditEntryName.setText(fetch_data[1])
            self.comboBoxEditEntryStatus.setCurrentText(fetch_data[2])
            self.spinBoxEditEntryQuantity.setValue(fetch_data[3])
            self.lineEditEntryDescription.setPlainText(fetch_data[4])
            self.dateEditEntryDate.setDate(fetch_data[5])
            self.comboBoxEditEntryEmployee.setCurrentText(fetch_data[6])
        except Exception as error:
            self.error_popup("Input Error", str(error))
        self.db.close()

    # Method to edit the entry
    def EditEntry_edit(self):
        edit_id = int(self.lineEditEntryId.text())
        entry_employee = self.comboBoxEditEntryEmployee.currentText()
        entry_status = self.comboBoxEditEntryStatus.currentText()
        entry_quantity = self.spinBoxEditEntryQuantity.value()
        entry_date = self.dateEditEntryDate.text()
        entry_description = self.lineEditEntryDescription.toPlainText()
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            try:
                self.cur.execute('''UPDATE entry SET  entry_status = %s, entry_qty = %s, entry_desc = %s, entry_date 
                = %s, entry_employee = %s WHERE id = %s''', (entry_status, entry_quantity, entry_description,
                                                             entry_date, entry_employee, edit_id))
            except Exception as error:
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.error_popup("Input Error", "Fail to update Entry.")
            else:
                self.cur.execute('RELEASE SAVEPOINT SP1')
                self.db.commit()
                self.success_popup("Entry", "Successfully updated Entry.")
        except Exception as error:
            self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
            self.error_popup("Input Error", "Fail to connect database.")
        self.db.close()

    # Method to undo the entry
    def EditEntry_undo(self):
        edit_id = int(self.lineEditEntryId.text())
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('''SELECT entry.id, part.part_name, entry.entry_status, entry.entry_qty, 
            entry.entry_desc, entry.entry_date, entry.entry_employee FROM entry JOIN part ON entry.part_id = part.id 
            WHERE entry.id = %s''', [(edit_id,)])
            fetch_data = self.cur.fetchone()
            self.lineEditEntryName.setText(fetch_data[1])
            self.comboBoxEditEntryStatus.setCurrentText(fetch_data[4])
            self.spinBoxEditEntryQuantity.setValue(fetch_data[3])
            self.lineEditEntryDescription.setPlainText(fetch_data[2])
            self.dateEditEntryDate.setDate(fetch_data[5])
            self.comboBoxEditEntryEmployee.setCurrentText(fetch_data[6])
        except Exception as error:
            self.error_popup("Input Error", "Failed to undo Entry details.")
        self.db.close()

    # Method to delete the part
    def EditEntry_delete(self):
        edit_id = int(self.lineEditEntryId.text())
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            try:
                self.cur.execute('''DELETE FROM entry WHERE id = %s''', [(edit_id,)])
            except IntegrityError as error:
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.error_popup("Input Error", "Entry cannot be deleted due to part data of the entry exists.")
            else:
                self.cur.execute('RELEASE SAVEPOINT SP1')
                self.db.commit()
                self.success_popup("Entry", "Successfully deleted Entry.")
        except Exception as error:
            self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
            self.error_popup("Input Error", "Failed to delete Entry.")
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

    # Method to confirm update entry
    def save_action(self):
        action = QMessageBox.warning(self, 'Update Entry', "Are you sure want to save the changes? Changes cannot be undo!", QMessageBox.Yes | QMessageBox.No)
        if action == QMessageBox.Yes:
            self.EditEntry_edit()
        else:
            pass

    # Method to confirm delete entry
    def delete_action(self):
        action = QMessageBox.warning(self, 'Delete Entry', "Are you sure want to delete? Changes cannot be undo!", QMessageBox.Yes | QMessageBox.No)
        if action == QMessageBox.Yes:
            self.EditEntry_delete()
        else:
            pass