from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from psycopg2 import IntegrityError
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
        self.HandleButtonAction()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonNewPartAdd.clicked.connect(self.AddPart_validate)
        self.pushButtonNewPartReset.clicked.connect(self.AddPart_reset)

    # Method to show drop-down data
    def ShowDepartment_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT department_name FROM department ORDER BY department_name ASC')
        department_list = self.cur.fetchall()
        for department in department_list:
            self.comboBoxNewPartDepartment.addItem(department[0])
        self.db.close()

    def ShowCategory_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT category_name FROM category ORDER BY category_name ASC')
        category_list = self.cur.fetchall()
        for category in category_list:
            self.comboBoxNewPartCategory.addItem(category[0])
        self.db.close()

    def ShowStorage_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT storage_name FROM storage ORDER BY storage_name ASC')
        storage_list = self.cur.fetchall()
        for storage in storage_list:
            self.comboBoxNewPartStorage.addItem(storage[0])
        self.db.close()

    # Method to validate empty field data entry
    def AddPart_validate(self):
        if not self.lineNewPartName.text() == '':
            if not self.lineNewPartManufacturer.text() == '':
                if not self.lineNewPartModel.text() == '':
                    if not self.lineNewPartDescription.toPlainText() == '':
                        self.AddPart_Data()
                    else:
                        self.error_popup("Input Error", "Invalid input or empty Description field")
                else:
                    self.error_popup("Input Error", "Invalid input or empty Model field")
            else:
                self.error_popup("Input Error", "Invalid input or empty Manufacturer field")
        else:
            self.error_popup("Input Error", "Invalid input or empty Name field")

    # Method to reset all add part fields
    def AddPart_reset(self):
        self.lineNewPartName.clear()
        self.comboBoxNewPartDepartment.clear()
        self.lineNewPartManufacturer.clear()
        self.lineNewPartModel.clear()
        self.comboBoxNewPartCategory.clear()
        self.comboBoxNewPartStorage.clear()
        self.spinBoxNewPartLimit.clear()
        self.lineNewPartDescription.clear()
        self.spinBoxNewPartLimit.setValue(1)
        self.ShowDepartment_custom()
        self.ShowStorage_custom()
        self.ShowCategory_custom()

    # Method to add part data
    def AddPart_Data(self):
        part_name = self.lineNewPartName.text()
        part_department = self.comboBoxNewPartDepartment.currentText()
        part_manufacturer = self.lineNewPartManufacturer.text()
        part_model = self.lineNewPartModel.text()
        part_category = self.comboBoxNewPartCategory.currentText()
        part_storage = self.comboBoxNewPartStorage.currentText()
        part_limit = self.spinBoxNewPartLimit.value()
        part_description = self.lineNewPartDescription.toPlainText()
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            try:
                self.cur.execute('''INSERT INTO part (part_name, part_department, part_manufacturer, part_model, part_category, part_storage, part_description, part_stocklimit) 
                                                    VALUES (%s , %s , %s , %s , %s , %s , %s , %s)''', (part_name, part_department, part_manufacturer, part_model, part_category, part_storage, part_description, part_limit))
            except IntegrityError as error:
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.AddPart_reset()
                self.error_popup("Duplicate Error", "Name of part already exists! Please use different name")
            else:
                self.cur.execute('RELEASE SAVEPOINT SP1')
                self.db.commit()
                self.AddPart_reset()
                self.success_popup("Part", "New Part Added.")
        except Exception as error:
            self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
            self.AddPart_reset()
            self.error_popup("Input Error", "Failed to add part.")
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