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
        self.signframe.setVisible(False)
        self.loginbtn.clicked.connect(self.loginFunction)
        self.signbtn.clicked.connect(self.signup)
        self.blur()
        self.accountbtn.clicked.connect(self.createAccount)
        self.accountbtn_2.clicked.connect(self.loginAccount)
        self.photobtn.clicked.connect(self.getfile)        

    def loginFunction(self):
        rollno = self.rollno.text()
        password = self.password.text()
        print("Successfully logged in with rollno - ",rollno,"and password - ",password)


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

    def signup(self):

        print("hiaaa")
        self.connectDB()



    def connectDB(self):
        try:
            connection = mysql.connector.connect(host='sql12.freesqldatabase.com', database='sql12394903',
                                                 user='sql12394903', password='WNRjtUUQWr', port='3306')
            cursor = connection.cursor()

            name = self.name.text()
            email = self.email.text()
            password = self.password_2.text()
            rollno = self.rollno_2.text()
            mySql_Create_Table_Query = " insert into user (name,email,password,rollno) VALUES(%s,%s,%s,%s)"
            value =(name,email,password,rollno)
            if(name=='' or email=='' or password=='' or rollno==''):
                m = QMessageBox.about(self, "warning","Pls fill all data")

            else:
                cursor.execute(mySql_Create_Table_Query, value)
                connection.commit()
                print("Data inserted")



            # result = cursor.fetchall()
            # for x in result:
            #     print(x)

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
            # print("hello")
            # connection = mysql.connector.connect(host='sql12.freesqldatabase.com',database='sql12394903',user='sql12394903',password='WNRjtUUQWr',port='3306')
            # cursor = connection.cursor()
            # print("hi")

            sql1 = """SELECT * FROM user"""

           # sql = ("INSERT INTO user (name,email,password,type,photo,rollno) VALUES(%s,%s,%s,%s,%s,%s)",
            #       (self.name.get(),
             #       self.email.get(),
              #      self.password_2.get(),
               #     self.type.get(),
                #    self.rollno_2.get()
                 #   ))

        #     cursor.execute(sql1)
        #     result = cursor.fetchall()
        #     for x in result:
        #         print(x)
        #     connection.commit()
        #     connection.close()
        #     messagebox.showinfo("Sucesss",parent = self.root)
        #     print("MySQL connection is closed with data inserted")
        #
        # except mysql.connector.Error as error:
        #     print("Failed to create table in MySQL: {}".format(error))
        #
        #

app = QApplication(sys.argv)
mainwindow = Login()
widgets = QtWidgets.QStackedWidget()
widgets.addWidget(mainwindow)
widgets.setFixedWidth(1200)
widgets.setFixedHeight(800)
widgets.show()
app.exec_()