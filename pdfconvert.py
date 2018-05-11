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
    def __init__(self): #initialize the app
        super().__init__()
        self.initUI()

    def initUI(self):
        ''' This function is the main UI of the application '''
        self.setWindowTitle("pdftocsvconverter") #setting the name of the app
        #self.setWindowIcon(QIcon(":/logo_tracker.png"))
        self.resize(280, 170)
  
        centralwidget = QWidget(self)
        
        #adding push buttons
        self.btn_file = QPushButton("PDF File", self)
        self.btn_file.clicked.connect(self.openFileNameDialog) #connecting methods/events to the buttons

        self.btn_convert = QPushButton("Convert", self)
        self.btn_convert.clicked.connect(self.Convert)
        #self.btn_convert.setEnabled(False)

        self.btn_showFile = QPushButton("Show File", self)
        self.btn_showFile.clicked.connect(self.showFile)

        self.btn_getPages = QPushButton("Pages", self) 
        self.btn_getPages.clicked.connect(self.getPages)

        self.cb_time_series = QCheckBox('Split Single Cell Values', self) #checkbox for split single cell values feature.
        self.cb_euro_delim = QCheckBox('Euro Decimal', self) #checkbox for euro feature.
        
        #self.cb_time_series.stateChanged.connect(self.state_changed)
        
    


        #initializing layout
        grid = QGridLayout()
        #adding the coordinates of each buttons and checkboxes
        grid.addWidget(self.btn_file, 1, 0)
        grid.addWidget(self.btn_convert, 3, 0)
        grid.addWidget(self.btn_showFile, 4, 0)
        grid.addWidget(self.btn_getPages, 2, 0)
        grid.addWidget(self.cb_time_series, 5, 0)
        grid.addWidget(self.cb_euro_delim, 6, 0)
        
        

        self.statusBar() #adding a statusbar for converting files

        centralwidget.setLayout(grid) #adding grid to the setlayout method of centralwidget 
        self.setCentralWidget(centralwidget)
        self.center() 
        self.show() #show the UI
    
    
    usefile="" #initialize with an empty string

    def openFileNameDialog(self):    
        '''This function will handle the event for the PDF Files selection from the directory.'''
        options = QFileDialog.Options() #setting options
        fileName, _ = QFileDialog.getOpenFileName(self,"Current Working Directory", "","PDF Files (*.pdf)", options=options)
        
        if fileName:
            global usefile
            usefile = fileName
            QMessageBox.information(self, 'Message', "File used: %s" % usefile) #adding information for the user
        #    self.getPages()
            #self.btn_convert.setEnabled(True)
            return self.make_directory() #make the directory for the output file.
        
        else:
            QMessageBox.information(self, 'Warning', "You did not select a .pdf file") #error handling of the .pdf file selection if the user doesn't picked a pdf file.
            return self.openFileNameDialog() #return the openfilenamedialog when error comes
            
    def getPages(self):
        '''This function will handle the pages to be used in converting the pdf table. '''
        global page
        page, okPressed = QInputDialog.getText(self, "Message","Pages:", QLineEdit.Normal, "") #set user page specification.
        if okPressed and page != '':
            QMessageBox.information(self, 'Message', "Pages used: %s" % page) #return pages that are used.
        else:
            return self.getPages() #return the function loop if error comes.

    def showFile(self):
        '''This function will return different output files. '''
        try: #show different files for different features used.
            if self.cb_time_series.isChecked(): #if the split single cell values is ticked run the time_series function then return the log.csv file.
                self.time_series()
                return os.startfile("C:/OutputFolder/time_series_transformed.csv")
            
            elif self.cb_euro_delim.isChecked():
                self.final_euro_delimiter()
                return os.startfile("C:/OutputFolder/transformed_euro.csv")
                
            else: #return the normal output.csv file
                self.statusBar().showMessage('') #show blank to remove the converted text in the statusbar
                return os.startfile("C:/OutputFolder/Output.csv")
                
            

        except: #exception handling, return information/hint for the user what to do.
            QMessageBox.information(self, 'Warning', "Hint: Close the output file")
    
    def Convert(self):
        '''This function will handle the converting process of the pdf tables using the convert_into function of the tabula-py'''
        try:
            tabula.convert_into("%s" % usefile, output_path="C:/OutputFolder/Output.csv", output_format="csv", pages ="%s" % page)
            self.statusBar().showMessage('Converted') #show when the file is already converted

        except:  #user hints for error handling                      
            QMessageBox.information(self, "WARNING", "Hint:Close the output file or Select the page.")


    def center(self):
        '''PyQt5 misc for frame geometry of UI'''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    
    def make_directory(self): 
        '''This function will make a directory.'''
        directory = "C:/OutputFolder/" #exact location of the directory.

        if not os.path.exists(directory): #if the directory doesnt exist, make a directory.
            os.makedirs(directory)


    #FEATURES
   
    def time_series(self):
        '''This function will solve the problem of the output file where there are multiple values in a single cell'''
        filename= "C:/OutputFolder/Output.csv" #specify the output csv as input file
        logfile = "C:/OutputFolder/time_series_transformed.csv" #specify the log.csv to be the second output file
        if os.path.exists(logfile): #if the log.csv exists, remove it.
            os.remove(logfile)
            
        with open("C:/OutputFolder/time_series_transformed.txt", "w", encoding="utf-8") as out_file: #create an output file with a txtfile to be converted into csv
            with open(filename, "r") as in_file: #load the Output.csv to be parsed and edited as a python object.
                reader = csv.reader(in_file, quoting=csv.QUOTE_MINIMAL) #using reader method of the csv module to iterate over the items in a list.
                #quote minimal is used to minimize quotation of the elements in the reader class.
                to_list = [] #instantiate a list
                for line in reader:
                    if self.cb_euro_delim.isChecked():
                        to_list.append("_".join(line) + "\n")     
                    else:
                        to_list.append(" ".join(line) + "\n") #join items in a list using space                
                to_str = []      
                for i in to_list:
                    if self.cb_euro_delim.isChecked():                                               
                        to_str.append(i.replace(",",".").replace(" ","")) #replace delimiter "," with blank to concatenate
                    else:                  
                        to_str.append(i.replace(",",""))               
                to_text = []
                for text in to_str:
                    if self.cb_euro_delim.isChecked():  
                        to_text.append(text.replace("_",","))
                    else:
                        to_text.append(text.replace(" ",",")) #replace spaces to the natural delimiter ","
                    #TO DO: use regex to find all text/dates/headers and then not include them on the text.replace(" ",",") exception.
                    #hint: text.replace(" ",",") if text not in headers
            out_file.writelines(to_text) #write the to_text list in the log.txt file
        os.rename("C:/OutputFolder/time_series_transformed.txt", "C:/OutputFolder/time_series_transformed.csv") #convert the textfile into csv file by renaming it.

    def final_euro_delimiter(self):
        '''This function solves the problem of the european delimiter of comma (,) as period (.)'''
        
        transformed_file = "C:/OutputFolder/transformed_euro.csv"
        filename= "C:/OutputFolder/Output.csv"
        if os.path.exists(transformed_file): #if the log.csv exists, remove it.
            os.remove(transformed_file)
        with open("C:/OutputFolder/transformed_euro.txt", "w", newline="", encoding="utf-8") as out_file: #create an output file with a txtfile to be converted into csv
            writer = csv.writer(out_file)
            with open(filename, "r") as in_file: #load the Output.csv to be parsed and edited as a python object.
                reader = csv.reader(in_file, quoting=csv.QUOTE_MINIMAL) #using reader method of the csv module to iterate over the items in a list.
                #quote minimal is used to minimize quotation of the elements in the reader class.
                to_list = [] #instantiate a list
                
                for line in reader:
                    to_list.append([x.replace(",",".").replace(" ","") for x in line])
                    
            writer.writerows(to_list)
        os.rename("C:/OutputFolder/transformed_euro.txt", "C:/OutputFolder/transformed_euro.csv")   

if __name__ == "__main__": #run the program
    app = QApplication(sys.argv)
    win = Converter()
    sys.exit(app.exec_())
