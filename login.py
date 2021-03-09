import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import mysql.connector
from mysql.connector import Error

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.setWindowTitle("OLES - Online Exam System")
        self.signframe.setVisible(False)
        self.loginbtn.clicked.connect(self.loginFunction)
        self.blur()
        self.accountbtn.clicked.connect(self.createAccount)
        self.accountbtn_2.clicked.connect(self.loginAccount)
        self.photobtn.clicked.connect(self.getfile)        

    def loginFunction(self):
        rollno = self.rollno.text()
        password = self.password.text()
        print("Successfully logged in with rollno - ",rollno,"and password - ",password)
        #self.connectDB()
        mainwindow = Application()
        widgets.addWidget(mainwindow)
        widgets.setCurrentIndex(widgets.currentIndex()+1)


    def createAccount(self):
        self.loginframe.setVisible(False)
        self.signframe.setVisible(True)

    def loginAccount(self):
        self.signframe.setVisible(False)
        self.loginframe.setVisible(True)
        
    def blur(self):	
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(30) 
        self.blurlbl.setGraphicsEffect(self.blur_effect)

    def getfile(self):
        fname, _= QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Image files (*.jpg *.png)")
        print(fname)
        self.photolbl.setPixmap(QPixmap(fname))

    def connectDB(self):
        try:
            connection = mysql.connector.connect(host='sql12.freesqldatabase.com',database='sql12394903',user='sql12394903',password='WNRjtUUQWr',port='3306')
            mySql_Create_Table_Query = """SELECT * FROM user"""
            cursor = connection.cursor()
            cursor.execute(mySql_Create_Table_Query)
            result = cursor.fetchall()
            for x in result:
                print(x)

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

class Application(QMainWindow):
    def __init__(self):
        super(Application,self).__init__()
        loadUi("application.ui",self)
        self.setWindowTitle("OLES - Online Exam System")
        self.blur()

    def blur(self):	
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(30) 
        self.blurlbl.setGraphicsEffect(self.blur_effect)

app = QApplication(sys.argv)
loginwindow = Login()
widgets = QtWidgets.QStackedWidget()
widgets.addWidget(loginwindow)
widgets.setFixedWidth(1200)
widgets.setFixedHeight(800)
widgets.show()
app.exec_()