import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import mysql.connector
from mysql.connector import Error
import base64
import io
from PIL import Image

connection = mysql.connector.connect(host='localhost', database='OnlineExamSystem', user='root', password='', port='3306')
cursor = connection.cursor()

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.setWindowTitle("OLES - Online Exam System")
        self.signframe.setVisible(False)
        self.rollno_3.setVisible(False)
        self.loginbtn.clicked.connect(self.loginFunction)
        self.blur()
        self.accountbtn.clicked.connect(self.createAccount)
        self.accountbtn_2.clicked.connect(self.loginAccount)
        self.photobtn.clicked.connect(self.getfile)
        self.signbtn.clicked.connect(self.signUp)        

    def loginFunction(self):
        rollno = self.rollno.text()
        password = self.password.text()

        sql = "select * from user where rollno = %s and password = %s"
        values = (rollno,password)
        cursor.execute(sql,values)
        result = cursor.fetchall()
        if result:            
            for x in result:
                mainwindow = Application()
                widgets.addWidget(mainwindow)
                widgets.setCurrentIndex(widgets.currentIndex()+1)
        else:
            print("Login failed")

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
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Image files (*.jpg *.png)",options=QFileDialog.DontUseNativeDialog)
        self.photolbl.setPixmap(QPixmap(fname))
        self.rollno_3.setText(fname)

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

    def signUp(self):
        name = self.name.text()
        rollno = self.rollno_2.text()
        email = self.email.text()
        password = self.password_2.text()
        confirmPass = self.password_3.text()
        type = "admin"

        with open (self.rollno_3.text(),"rb") as File:
            BinaryData = File.read()
        sql = "insert into user (rollno,name,email,type,password,photo) values (%s,%s,%s,%s,%s,%s)"
        value = (rollno,name,email,type,password,BinaryData)
        cursor.execute(sql,value)
        connection.commit()


class Application(QMainWindow):
    def __init__(self):
        super(Application,self).__init__()
        loadUi("application.ui",self)
        self.setWindowTitle("OLES - Online Exam System")
        self.blur()
        self.setUserInfo()

    def blur(self):	
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(30) 
        self.blurlbl.setGraphicsEffect(self.blur_effect)

    #def setUserInfo(self):
    #    cursor.execute('select photo from user where rollno = 5019114')
    #    data = cursor.fetchall()
    #    image = data[0][0]
    #    binary_data = base64.b64decode(image)
    #    image = Image.open(io.BytesIO(binary_data))
    #    image.show()         

app = QApplication(sys.argv)
loginwindow = Login()
widgets = QtWidgets.QStackedWidget()
widgets.addWidget(loginwindow)
widgets.setFixedWidth(1200)
widgets.setFixedHeight(800)
widgets.show()
app.exec_()
