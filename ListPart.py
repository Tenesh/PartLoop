from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import sys
import psycopg2
from PyQt5.uic import loadUiType
from Connect import ConnectDatabase

# Global Variable
listpart_ui, _ = loadUiType('Ui/ListPartLoop.ui')


class ListPartApp(QDialog, listpart_ui):
    def __init__(self, parent=None):
        super(ListPartApp, self).__init__(parent)
        self.setupUi(self)
        self.HandleButtonAction()
        self.ShowDepartment_custom()
        self.ShowCategory_custom()
        self.ShowStorage_custom()
        self.ClearDropDown()
        self.ListPart_show()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonListPartSearch.clicked.connect(self.ListPart_show)
        self.pushButtonListPartReset.clicked.connect(self.ListPart_reset)

    # Method to set empty value in drop-down field
    def ClearDropDown(self):
        self.comboBoxListPartDepartment.setCurrentText('')
        self.comboBoxListPartCategory.setCurrentText('')
        self.comboBoxListPartStorage.setCurrentText('')
        # self.comboBoxListPartStockLevel.setCurrentText('')

    # Method to show drop-down data
    def ShowDepartment_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT department_name FROM department ORDER BY department_name ASC')
        department_list = self.cur.fetchall()
        for department in department_list:
            self.comboBoxListPartDepartment.addItem(department[0])
        self.db.close()

    def ShowCategory_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT category_name FROM category ORDER BY category_name ASC')
        category_list = self.cur.fetchall()
        for category in category_list:
            self.comboBoxListPartCategory.addItem(category[0])
        self.db.close()

    def ShowStorage_custom(self):
        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT storage_name FROM storage ORDER BY storage_name ASC')
        storage_list = self.cur.fetchall()
        for storage in storage_list:
            self.comboBoxListPartStorage.addItem(storage[0])
        self.db.close()

    # Method to show list of part
    def ListPart_show(self):
        field_name = self.lineListPartName.text()
        field_department = self.comboBoxListPartDepartment.currentText()
        field_category = self.comboBoxListPartCategory.currentText()
        field_storage = self.comboBoxListPartStorage.currentText()
        # field_stocklevel = self.comboBoxListPartStockLevel.currentText()
        search_name = '%{}%'.format(field_name)
        search_department = '%{}%'.format(field_department)
        search_category = '%{}%'.format(field_category)
        search_storage = '%{}%'.format(field_storage)
        # search_stocklevel = '%{}%'.format(field_stocklevel)

        self.db = ConnectDatabase()
        self.cur = self.db.cursor()
        try:
            self.cur.execute('''SELECT part.id, part.part_name, part.part_department, part.part_manufacturer, part.part_model, part.part_category, part.part_storage, part.part_stocklimit, 
            SUM ( ( CASE 
                    WHEN entry.entry_status = 'In' THEN 1 
                    ELSE -1 END)*entry.entry_qty) AS stock_quantity,
            CASE 
                WHEN SUM( (CASE  WHEN entry.entry_status = 'In' THEN 1 ELSE -1 END)* entry.entry_qty) < part.part_stocklimit/2 THEN 'Critical'
                WHEN SUM( (CASE  WHEN entry.entry_status = 'In' THEN 1 ELSE -1 END)* entry.entry_qty) < part.part_stocklimit THEN 'Low'
                WHEN SUM( (CASE  WHEN entry.entry_status = 'In' THEN 1 ELSE -1 END)* entry.entry_qty) >= part.part_stocklimit THEN 'Normal'
                WHEN SUM( (CASE  WHEN entry.entry_status = 'In' THEN 1 ELSE -1 END)* entry.entry_qty) > part.part_stocklimit*2 THEN 'High'
                ELSE 'Normal' END AS stock_level,
            part.part_description
            FROM part 
            INNER JOIN entry ON entry.part_id = part.id 
            GROUP BY part.id
            HAVING part.part_name ILIKE %s AND part.part_department ILIKE %s AND part.part_category ILIKE %s AND part.part_storage ILIKE %s ORDER BY part.id ASC''',
                             (search_name, search_department, search_category, search_storage))
            fetch_data = self.cur.fetchall()
        except Exception as error:
            print(error)
            self.error_popup("Duplicate Error", str(error))
        else:
            if fetch_data is None:
                self.tableWidgetListPart.setRowCount(0)
                self.error_popup("List Part", "No records found!")
            else:
                self.tableWidgetListPart.horizontalHeader().setSectionResizeMode(0, 20)
                self.tableWidgetListPart.horizontalHeader().setSectionResizeMode(1, 20)
                self.tableWidgetListPart.setRowCount(0)
                self.tableWidgetListPart.insertRow(0)
                for row, form in enumerate(fetch_data):
                    for column, item in enumerate(form):
                        self.tableWidgetListPart.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1
                        row_position = self.tableWidgetListPart.rowCount()
                        self.tableWidgetListPart.insertRow(row_position)
                        self.tableWidgetListPart.resizeColumnsToContents()
                        self.tableWidgetListPart.horizontalHeader().setSectionResizeMode(10, QHeaderView.Stretch)
        self.db.close()

    # Method to reset list of entry
    def ListPart_reset(self):
        self.ClearDropDown()
        self.lineListPartName.clear()
        self.ListPart_show()

    # Method to show error popup window
    def error_popup(self, title_popup, msg_popup):
        popup = QMessageBox()
        popup.setFixedSize(500, 500)
        popup.setWindowTitle(title_popup)
        popup.setIcon(QMessageBox.Warning)
        popup.setStyleSheet("font:9pt Poppins;")
        popup.setText(msg_popup)
        popup.exec_()