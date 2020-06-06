from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from PyQt5.uic import loadUiType
from Connect import ConnectDatabase
from psycopg2 import IntegrityError

# Global Variable
editpart_ui, _ = loadUiType('Ui/EditPartLoop.ui')


class EditPartApp(QDialog, editpart_ui):
    def __init__(self, part_id, parent=None):
        super(EditPartApp, self).__init__(parent)
        self.setupUi(self)
        self.HandleButtonAction()
        self.ShowCategory_custom()
        self.ShowStorage_custom()
        self.ShowDepartment_custom()
        self.EditPart_search(part_id)
        self.lineEditPartId.setText(str(part_id))

    # Method to show drop-down data
    def ShowDepartment_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT department_name FROM department ORDER BY department_name ASC')
        department_list = self.cur.fetchall()
        for department in department_list:
            self.comboBoxEditPartDepartment.addItem(department[0])
        self.db.close()

    def ShowCategory_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT category_name FROM category ORDER BY category_name ASC')
        category_list = self.cur.fetchall()
        for category in category_list:
            self.comboBoxEditPartCategory.addItem(category[0])
        self.db.close()

    def ShowStorage_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT storage_name FROM storage ORDER BY storage_name ASC')
        storage_list = self.cur.fetchall()
        for storage in storage_list:
            self.comboBoxEditPartStorage.addItem(storage[0])
        self.db.close()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonEditPartSave.clicked.connect(self.save_action)
        self.pushButtonEditPartUndo.clicked.connect(self.EditPart_undo)
        self.pushButtonEditPartDelete.clicked.connect(self.delete_action)

    # Method to search the part
    def EditPart_search(self, part_id):
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('''SELECT * FROM part WHERE id = %s''', [(part_id,)])
            fetch_data = self.cur.fetchone()
            self.lineEditPartName.setText(fetch_data[1])
            self.comboBoxEditPartDepartment.setCurrentText(fetch_data[2])
            self.lineEditPartManufacturer.setText(fetch_data[3])
            self.lineEditPartModel.setText(fetch_data[4])
            self.comboBoxEditPartCategory.setCurrentText(fetch_data[5])
            self.comboBoxEditPartStorage.setCurrentText(fetch_data[6])
            self.spinBoxEditPartLimit.setValue(fetch_data[8])
            self.lineEditPartDescription.setPlainText(fetch_data[7])
        except Exception as error:
            self.error_popup("Input Error", "Part not found.")
        self.db.close()

    # Method to edit the part
    def EditPart_edit(self):
        edit_id = int(self.lineEditPartId.text())
        part_name = self.lineEditPartName.text()
        part_department = self.comboBoxEditPartDepartment.currentText()
        part_manufacturer = self.lineEditPartManufacturer.text()
        part_model = self.lineEditPartModel.text()
        part_category = self.comboBoxEditPartCategory.currentText()
        part_storage = self.comboBoxEditPartStorage.currentText()
        part_limit = self.spinBoxEditPartLimit.value()
        part_description = self.lineEditPartDescription.toPlainText()
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            try:
                self.cur.execute('''UPDATE part SET part_name = %s, part_department = %s, part_manufacturer = %s, 
                part_model = %s, part_category = %s, part_storage = %s, part_description = %s, part_stocklimit = %s WHERE 
                id = %s''', (part_name, part_department, part_manufacturer, part_model, part_category, part_storage,
                             part_description, part_limit, edit_id))
            except Exception as error:
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.error_popup("Input Error", "Fail to update Part.")
            else:
                self.cur.execute('RELEASE SAVEPOINT SP1')
                self.db.commit()
                self.success_popup("Part", "Successfully updated Part.")
        except Exception as error:
            self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
            self.error_popup("Input Error", "Fail to connect database.")
        self.db.close()

    # Method to undo the part
    def EditPart_undo(self):
        edit_id = int(self.lineEditPartId.text())
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('''SELECT * FROM part where id = %s''', [(edit_id,)])
            fetch_data = self.cur.fetchone()
            self.lineEditPartName.setText(fetch_data[1])
            self.comboBoxEditPartDepartment.setCurrentText(fetch_data[2])
            self.lineEditPartManufacturer.setText(fetch_data[3])
            self.lineEditPartModel.setText(fetch_data[4])
            self.comboBoxEditPartCategory.setCurrentText(fetch_data[5])
            self.comboBoxEditPartStorage.setCurrentText(fetch_data[6])
            self.spinBoxEditPartLimit.setValue(fetch_data[8])
            self.lineEditPartDescription.setPlainText(fetch_data[7])
        except Exception as error:
            self.error_popup("Input Error", "Failed to undo Part.")
        self.db.close()

    # Method to delete the part
    def EditPart_delete(self):
        edit_id = int(self.lineEditPartId.text())
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            try:
                self.cur.execute('''DELETE FROM part WHERE id = %s''', [(edit_id,)])
            except IntegrityError as error:
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.error_popup("Input Error", "Part cannot be deleted due to entry data of the part exists.")
            else:
                self.cur.execute('RELEASE SAVEPOINT SP1')
                self.db.commit()
                self.success_popup("Part", "Successfully deleted Part.")
        except Exception as error:
            self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
            self.error_popup("Input Error", "Failed to delete Part.")
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

    # Method to confirm update part
    def save_action(self):
        action = QMessageBox.warning(self, 'Update Part', "Are you sure want to save the changes? Changes cannot be undo!", QMessageBox.Yes | QMessageBox.No)
        if action == QMessageBox.Yes:
            self.EditPart_edit()
        else:
            pass

    # Method to confirm delete part
    def delete_action(self):
        action = QMessageBox.warning(self, 'Delete Part', "Are you sure want to delete? Changes cannot be undo!", QMessageBox.Yes | QMessageBox.No)
        if action == QMessageBox.Yes:
            self.EditPart_delete()
        else:
            pass