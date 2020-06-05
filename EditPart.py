from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from PyQt5.uic import loadUiType
from Connect import ConnectDatabase

editpart_ui, _ = loadUiType('Ui/EditPartLoop.ui')


class EditPartApp(QDialog, editpart_ui):
    def __init__(self, part_id, parent=None):
        super(EditPartApp, self).__init__(parent)
        self.setupUi(self)
        # self.HandleButtonAction()
        self.ShowCategory_custom()
        self.ShowStorage_custom()
        self.ShowDepartment_custom()
        self.EditPart_search(part_id)

    # Method to show drop-down data
    def ShowDepartment_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT department_name FROM department')
        department_list = self.cur.fetchall()
        for department in department_list:
            self.comboBoxEditPartDepartment.addItem(department[0])
        self.db.close()

    def ShowCategory_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT category_name FROM category')
        category_list = self.cur.fetchall()
        for category in category_list:
            self.comboBoxEditPartCategory.addItem(category[0])
        self.db.close()

    def ShowStorage_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT storage_name FROM storage')
        storage_list = self.cur.fetchall()
        for storage in storage_list:
            self.comboBoxEditPartStorage.addItem(storage[0])
        self.db.close()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonEditPartSave.clicked.connect(self.EditPart_edit)
        self.pushButtonEditPartUndo.clicked.connect(self.EditPart_undo)
        self.pushButtonEditPartDelete.clicked.connect(self.EditPart_delete)

    # Method to search the part
    def EditPart_search(self, part_id):
        try:
            self.db = ConnectDatabase()
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            self.cur.execute('''SELECT * FROM part where id = %s''', [(part_id,)])
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
            self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
            self.error_popup("Input Error", "Part not found.")
        self.db.close


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
