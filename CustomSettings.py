from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from Connect import ConnectDatabase
from PyQt5.uic import loadUiType

# Global Variables
custom_ui, _ = loadUiType('Ui/CustomPartLoop.ui')


class CustomApp(QDialog, custom_ui):
    def __init__(self, parent=None):
        super(CustomApp, self).__init__(parent)
        self.setupUi(self)
        self.HandleButtonAction()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonCustomDepartmentAdd.clicked.connect(self.AddDepartment_validate)
        self.pushButtonCustomStorageAdd.clicked.connect(self.AddStorage_validate)
        self.pushButtonCustomCategoryAdd.clicked.connect(self.AddCategory_validate)
        self.pushButtonCustomEmployeeAdd.clicked.connect(self.AddEmployee_validate)

    # Method to validate empty field for drop-down data
    def AddDepartment_validate(self):
        if not self.lineCustomDepartment.text() == '':
            self.AddDepartment_custom()
        else:
            self.error_popup("Input Error", "Invalid or empty input in Department field")

    def AddStorage_validate(self):
        if not self.lineCustomStorage.text() == '':
            self.AddStorage_custom()
        else:
            self.error_popup("Input Error", "Invalid or empty input in Storage field.")

    def AddCategory_validate(self):
        if not self.lineCustomCategory.text() == '':
            self.AddCategory_custom()
        else:
            self.error_popup("Input Error", "Invalid or empty input in Category field.")

    def AddEmployee_validate(self):
        if not self.lineCustomEmployee.text() == '':
            self.AddEmployee_custom()
        else:
            self.error_popup("Input Error", "Invalid or empty input in Employee field.")

    # Method to add drop-down data
    def AddDepartment_custom(self):
        department_name = self.lineCustomDepartment.text()
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            try:
                self.cur.execute('INSERT INTO department (department_name) VALUES (%s)', (department_name,))
            except psycopg2.IntegrityError:
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.lineCustomDepartment.clear()
                self.error_popup("Duplicate Input", "Department already exist. Please enter different input.")
            else:
                self.cur.execute('RELEASE SAVEPOINT SP1')
                self.db.commit()
                self.lineCustomDepartment.clear()
                self.success_popup("Department", "New Department Added.")
            self.db.close()
        except Exception as error:
            self.lineCustomDepartment.clear()
            self.error_popup("Input Error", "Failed to add department")

    def AddStorage_custom(self):
        storage_name = self.lineCustomStorage.text()
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            try:
                self.cur.execute('INSERT INTO storage (storage_name) VALUES (%s)', (storage_name,))
            except psycopg2.IntegrityError:
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.lineCustomStorage.clear()
                self.error_popup("Duplicate Input", "Storage already exist. Please enter different input.")
            else:
                self.cur.execute('RELEASE SAVEPOINT SP1')
                self.db.commit()
                self.lineCustomStorage.clear()
                self.success_popup("Storage", "New Storage Added.")
            self.db.close()
        except Exception as error:
            self.lineCustomStorage.clear()
            self.error_popup("Input Error", "Failed to add storage")

    def AddCategory_custom(self):
        category_name = self.lineCustomCategory.text()
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            try:
                self.cur.execute('INSERT INTO category (category_name) VALUES (%s)', (category_name,))
            except psycopg2.IntegrityError:
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.lineCustomCategory.clear()
                self.error_popup("Duplicate Input", "Category already exist. Please enter different input.")
            else:
                self.cur.execute('RELEASE SAVEPOINT SP1')
                self.db.commit()
                self.lineCustomCategory.clear()
                self.success_popup("Category", "New Category Added.")
            self.db.close()
        except Exception as error:
            self.lineCustomCategory.clear()
            self.error_popup("Input Error", "Failed to add category")

    def AddEmployee_custom(self):
        employee_name = self.lineCustomEmployee.text()
        self.db = ConnectDatabase()
        try:
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            try:
                self.cur.execute('INSERT INTO employee (employee_name) VALUES (%s)', (employee_name,))
            except psycopg2.IntegrityError:
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.lineCustomEmployee.clear()
                self.error_popup("Duplicate Input", "Employee already exist. Please enter different input.")
            else:
                self.cur.execute('RELEASE SAVEPOINT SP1')
                self.db.commit()
                self.lineCustomEmployee.clear()
                self.success_popup("Employee", "New Employee Added.")
            self.db.close()
        except Exception as error:
            self.lineCustomEmployee.clear()
            self.error_popup("Input Error", "Failed to add employee")

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