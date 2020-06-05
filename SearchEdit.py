from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from psycopg2 import IntegrityError
from Connect import ConnectDatabase
from PyQt5.uic import loadUiType
from EditPart import EditPartApp
from EditEntry import EditEntryApp

# Global Variable
searcheditpart_ui, _ = loadUiType('Ui/SearchEditPartLoop.ui')
searcheditentry_ui, _ = loadUiType('Ui/SearchEditEntryPartLoop.ui')


# Class for searching edit part
class SearchEditPartApp(QDialog, searcheditpart_ui):
    def __init__(self, parent=None):
        super(SearchEditPartApp, self).__init__(parent)
        self.setupUi(self)
        self.HandleButtonAction()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonSearchEditPartIdSearch.clicked.connect(self.SearchEditPart_search)

    def SearchEditPart_search(self):
        search_id = self.lineSearchEditId.text()
        try:
            part_id = int(search_id)  # Convert text into integer
        except Exception as error:
            self.error_popup("Input Error", "Please enter numbers only.")
        else:
            self.db = ConnectDatabase()
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            self.cur.execute('''SELECT * FROM part where id = %s''', [(part_id,)])  # Check if part id available in db
            fetch_data = self.cur.fetchone()
            if fetch_data is None:  # If returns None or Id not in database
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.error_popup("Invalid Input", "Part not registered.")
            else:
                self.EditPart_window(part_id)
        self.db.close

    # Method to open Edit Part window
    def EditPart_window(self, part_id):
        self.apw = EditPartApp(part_id)
        self.apw.show()

    # Method to show error popup window
    def error_popup(self, title_popup, msg_popup):
        popup = QMessageBox()
        popup.setFixedSize(500, 500)
        popup.setWindowTitle(title_popup)
        popup.setIcon(QMessageBox.Warning)
        popup.setStyleSheet("font:9pt Poppins;")
        popup.setText(msg_popup)
        popup.exec_()


# Class for searching edit entry
class SearchEditEntryApp(QDialog, searcheditentry_ui):
    def __init__(self, parent=None):
        super(SearchEditEntryApp, self).__init__(parent)
        self.setupUi(self)
        self.HandleButtonAction()

    # Method for Button action
    def HandleButtonAction(self):
        self.pushButtonSearchEditEntryIdSearch.clicked.connect(self.SearchEditEntry_search)

    def SearchEditEntry_search(self):
        search_id = self.lineSearchEditId.text()
        try:
            entry_id = int(search_id)  # Convert text into integer
        except Exception as error:
            self.error_popup("Input Error", "Please enter numbers only.")
        else:
            self.db = ConnectDatabase()
            self.cur = self.db.cursor()
            self.cur.execute('SAVEPOINT SP1')
            self.cur.execute('''SELECT * FROM entry where id = %s''', [(entry_id,)])  # Check if part id available in db
            fetch_data = self.cur.fetchone()
            if fetch_data is None:  # If returns None or Id not in database
                self.cur.execute('ROLLBACK TO SAVEPOINT SP1')
                self.error_popup("Invalid Input", "Entry not registered.")
            else:
                print(fetch_data[2])
                print(len(fetch_data[2]))
                # self.EditEntry_window(entry_id)
        self.db.close

    # Method to open Edit Entry window
    def EditEntry_window(self, entry_id):
        self.apw = EditEntryApp(entry_id)
        self.apw.show()

    # Method to show error popup window
    def error_popup(self, title_popup, msg_popup):
        popup = QMessageBox()
        popup.setFixedSize(500, 500)
        popup.setWindowTitle(title_popup)
        popup.setIcon(QMessageBox.Warning)
        popup.setStyleSheet("font:9pt Poppins;")
        popup.setText(msg_popup)
        popup.exec_()