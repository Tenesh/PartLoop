from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from PyQt5.uic import loadUiType
from AddEntry import AddEntryApp
from AddPart import AddPartApp
from EditEntry import EditEntryApp
from EditPart import EditPartApp
from ListEntry import ListEntryApp
from ListPart import ListPartApp
from CustomSettings import CustomApp

# Global Variable
main_ui, _ = loadUiType('Ui/PartLoop.ui')


# Main Window Class
class MainApp(QMainWindow, main_ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.HandleMenuAction()

    # Main Method for MenuBar action
    def HandleMenuAction(self):
        self.actionNewPart_3.triggered.connect(self.AddPart_window)
        self.actionNewEntry_3.triggered.connect(self.AddEntry_window)
        self.actionEditPart_2.triggered.connect(self.EditPart_window)
        self.actionEditEntry_2.triggered.connect(self.EditEntry_window)
        self.actionListPart.triggered.connect(self.ListPart_window)
        self.actionListEntry.triggered.connect(self.ListEntry_window)
        self.actionCustom.triggered.connect(self.Custom_window)
        # self.actionQuit.triggered.connect(self.QuitApp)
        # self.actionHelpAbout.triggered.connect(self.About)
        # self.actionHelpDocumentation.triggered.connect(self.Docs)
        # self.actionStatistics.triggered.connect(self.Statistic_window)

    # Main Method for passing QDialog Classes
    def AddPart_window(self):
        self.apw = AddPartApp()
        self.apw.show()

    def EditPart_window(self):
        self.apw = EditPartApp()
        self.apw.show()

    def AddEntry_window(self):
        self.apw = AddEntryApp()
        self.apw.show()

    def EditEntry_window(self):
        self.apw = EditEntryApp()
        self.apw.show()

    def ListPart_window(self):
        self.apw = ListPartApp()
        self.apw.show()

    def ListEntry_window(self):
        self.apw = ListEntryApp()
        self.apw.show()

    def Custom_window(self):
        self.apw = CustomApp()
        self.apw.show()

# Running application
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()


