"Credits to Michiaki Ariga (https://github.com/chezou) for developing the AMAZING open-source tabula-java wrapper called tabula-py"


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import time
import datetime
import tabula
#import image_qr
#from pandas import read_sql


class Converter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDFConverter")
        #self.setWindowIcon(QIcon(":/logo_tracker.png"))
        self.resize(280, 170)
  
        centralwidget = QWidget(self)
        

        self.btn_file = QPushButton("PDF File", self)
        self.btn_file.clicked.connect(self.openFileNameDialog)

        self.btn_convert = QPushButton("Convert", self)
        self.btn_convert.clicked.connect(self.Convert)
        #self.btn_convert.setEnabled(False)

        self.btn_showFile = QPushButton("Show File", self)
        self.btn_showFile.clicked.connect(self.showFile)

        self.btn_getPages = QPushButton("Pages", self)
        self.btn_getPages.clicked.connect(self.getPages)




        



        grid = QGridLayout()

        grid.addWidget(self.btn_file, 1, 0)
        grid.addWidget(self.btn_convert, 3, 0)
        grid.addWidget(self.btn_showFile, 4, 0)
        grid.addWidget(self.btn_getPages, 2, 0)

        self.statusBar()

        centralwidget.setLayout(grid)
        self.setCentralWidget(centralwidget)
        self.center()
        self.show()
    

    usefile=""
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Current Working Directory", "","PDF Files (*.pdf)", options=options)
        
        if fileName:
            global usefile
            usefile = fileName
            QMessageBox.information(self, 'Message', "File used: %s" % usefile)
        #    self.getPages()
            #self.btn_convert.setEnabled(True)
            self.make_directory()
        
        else:
            QMessageBox.information(self, 'Warning', "You did not select a .pdf file")
            self.openFileNameDialog()
            
    def getPages(self):
        global page
        page, okPressed = QInputDialog.getText(self, "Message","Pages:", QLineEdit.Normal, "")
        if okPressed and page != '':
            QMessageBox.information(self, 'Message', "Pages used: %s" % page)
        else:
            self.getPages()

    def showFile(self):
        try:
            os.startfile("C:/OutputFolder/Output.csv")
            self.statusBar().showMessage('')
        except:
            QMessageBox.information(self, 'Warning', "Output file not created!")

    def Convert(self):
        try:
            tabula.convert_into("%s" % usefile, output_path="C:/OutputFolder/Output.csv", output_format="csv", pages ="%s" % page)
            self.statusBar().showMessage('Converted')

        except:                        
            QMessageBox.information(self, "WARNING", "Close the output file or Select the page!")


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    
    
    def make_directory(self):
        directory = "C:/OutputFolder/"
        if not os.path.exists(directory):
            os.makedirs(directory)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Converter()
    sys.exit(app.exec_())
