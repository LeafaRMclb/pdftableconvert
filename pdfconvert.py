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
import csv

#import image_qr
#from pandas import read_sql


class Converter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("pdftocsvconverter")
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

        self.cb_time_series = QCheckBox('Split Single Cell Values', self)
        self.cb_euro_delim = QCheckBox('Euro Delimiter', self)
        
        #self.cb_time_series.stateChanged.connect(self.state_changed)
        
    



        grid = QGridLayout()

        grid.addWidget(self.btn_file, 1, 0)
        grid.addWidget(self.btn_convert, 3, 0)
        grid.addWidget(self.btn_showFile, 4, 0)
        grid.addWidget(self.btn_getPages, 2, 0)
        grid.addWidget(self.cb_time_series, 5, 0)
        grid.addWidget(self.cb_euro_delim, 6, 0)
        
        

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
            if self.cb_time_series.isChecked():
                self.time_series()
                os.startfile("C:/OutputFolder/log.csv")
                
            else:
                os.startfile("C:/OutputFolder/Output.csv")
                self.statusBar().showMessage('')
            

        except Exception as e:
            QMessageBox.information(self, 'Warning', "%s" % e)

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
    
    def state_changed(self):
        if self.cb_time_series.isChecked():
            self.time_series()
            
        else:
            try:
                os.remove("C:/OutputFolder/log.csv")
            except:
                QMessageBox.information(self, "WARNING", "Hint: Close the output file")

#HELLO ROXANNE :)
    #FEATURES
    def time_series(self):
        filename= "C:/OutputFolder/Output.csv"
        logfile = "C:/OutputFolder/log.csv"
        if os.path.exists(logfile):
            os.remove(logfile)
        with open("C:/OutputFolder/log.txt", "w", encoding="utf-8") as out_file:
            with open(filename, "r") as in_file:
                reader = csv.reader(in_file, quoting=csv.QUOTE_MINIMAL)
                to_list = []
                
                for line in reader:
                    to_list.append(" ".join(line) + "\n") #join items in a list using space                
                to_str = []
                
                if self.cb_euro_delim.isChecked():                   
                    for i in to_list:                                 
                        to_str.append(i.replace(",",".")) #replace delimiter "," with blank to concatenate
                else:
                    for i in to_list:                                 
                        to_str.append(i.replace(","," "))
                    
                to_text = []
                for text in to_str:
                    to_text.append(text.replace(" ",",")) #replace spaces to the natural delimiter ","
                    #TO DO: use regex to find all text/dates/headers and then not include them on the text.replace(" ",",") exception.
                    #hint: text.replace(" ",",") if text not in headers
            out_file.writelines(to_text)
        os.rename("C:/OutputFolder/log.txt", "C:/OutputFolder/log.csv")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Converter()
    sys.exit(app.exec_())
