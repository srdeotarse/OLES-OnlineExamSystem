import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import mysql.connector
from mysql.connector import Error
import base64
import io
from PIL import Image
from PIL.ImageQt import ImageQt

connection = mysql.connector.connect(host='localhost', database='OnlineExamSystem', user='root', password='', port='3306')
cursor = connection.cursor()

class Login(QDialog):
    def __init__(self,master):
        self.master = master
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

        reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QRegExpValidator(reg_ex, self.rollno)
        self.rollno.setValidator(input_validator)      

    def loginFunction(self):
        self.rollNo = self.rollno.text()
        password = self.password.text()
        type = self.typeCombo.currentText();      

        sql = "select * from user where rollno = %s and password = %s and type = %s"
        values = (self.rollNo,password,type)
        cursor.execute(sql,values)
        result = cursor.fetchall()
        if result:            
            for x in result:
                mainwindow = Application(self.rollNo)
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
        type = self.typeCombo_2.currentText()

        with open (self.rollno_3.text(),"rb") as File:
            BinaryData = File.read()

        sql = "insert into user (rollno,name,email,type,password,photo) values (%s,%s,%s,%s,%s,%s)"
        value = (rollno,name,email,type,password,BinaryData)

        if (rollno.isdigit() == False):
            m = QMessageBox.about(self, "warning", "Please Enter a Roll Number in Digits")

        elif (len(rollno) < 7):
            m = QMessageBox.about(self, "warning", "Please Enter a Roll Number of Length 7 Digits")

        elif (len(password)<8):
            m = QMessageBox.about(self, "warning", "Please Enter a Strong Password")

        elif (confirmPass != password):
            m = QMessageBox.about(self, "warning", "Please Enter Correct Password")

        elif (name == '' or email == '' or password == '' or rollno == '' or self.rollno_3.text() == ''):
            m = QMessageBox.about(self, "warning", "Please fill all the data")

        else:
            cursor.execute(sql,value)
            connection.commit()
            m = QMessageBox.about(self, "SUCCESS!", "ACCOUNT CREATED!")


class Application(QMainWindow,Login):
    def __init__(self,rollNo):
        super(Application,self).__init__(rollNo)
        loadUi("application.ui",self)
        self.setWindowTitle("OLES - Online Exam System")
        self.blur()
        self.userrollno.setText(rollNo)
        self.setUserInfo()
        self.resultsframe.setVisible(False)
        self.createframe.setVisible(False)
        self.adduserframe.setVisible(False)
        self.settingsframe.setVisible(False)
        self.feedbackframe.setVisible(False)
        self.dashboardbtn.clicked.connect(self.showDashboard)
        self.resultsbtn.clicked.connect(self.showResults)
        self.settingsbtn.clicked.connect(self.showSettings)
        self.createexambtn.clicked.connect(self.showCreate)
        self.adduserbtn.clicked.connect(self.showAddUser)
        self.feedbackbtn.clicked.connect(self.showFeedback)  
        self.startexambtn.clicked.connect(self.startExam)      

    def blur(self):	
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(30) 
        self.blurlbl.setGraphicsEffect(self.blur_effect)

    def setUserInfo(self):
        sql = "select * from user where rollno = %s"
        values = (self.userrollno.text(),)
        cursor.execute(sql,values)
        myresult = cursor.fetchone()
        StoreFilepath = "img/image.jpg"
        with open(StoreFilepath, "wb") as file:
            file.write(myresult[6])
            file.close()
        self.userphoto.setPixmap(QPixmap("img/image.jpg"))
        self.username.setText(myresult[2])
        self.usertype.setText(myresult[5])

    def setBtnBG(self,QLabel,QPushButton,Image):
        QLabel.setStyleSheet("background:#691A7F; border-radius:10px")
        QPushButton.setStyleSheet("color:white; text-align:left; padding-left:20px;")
        QPushButton.setIcon(Image)

    def showDashboard(self):
        self.dashboardframe.setVisible(True)
        self.resultsframe.setVisible(False)
        self.feedbackframe.setVisible(False)
        self.createframe.setVisible(False)
        self.adduserframe.setVisible(False)
        self.settingsframe.setVisible(False)
        self.currentExamsData()
        self.setBtnBG(self.dashboardbtnlbl,self.dashboardbtn,QtGui.QIcon('img/dashboard-white.png'))

    def showResults(self):
        self.dashboardframe.setVisible(False)
        self.resultsframe.setVisible(True)
        self.createframe.setVisible(False)
        self.adduserframe.setVisible(False)
        self.settingsframe.setVisible(False)
        self.feedbackframe.setVisible(False)

    def showFeedback(self):
        self.dashboardframe.setVisible(False)
        self.resultsframe.setVisible(False)
        self.createframe.setVisible(False)
        self.adduserframe.setVisible(False)
        self.settingsframe.setVisible(False)
        self.feedbackframe.setVisible(True)

    def showSettings(self):
        self.dashboardframe.setVisible(False)
        self.resultsframe.setVisible(False)
        self.createframe.setVisible(False)
        self.adduserframe.setVisible(False)
        self.settingsframe.setVisible(True)
        self.feedbackframe.setVisible(False)

    def showCreate(self):
        self.dashboardframe.setVisible(False)
        self.resultsframe.setVisible(False)
        self.createframe.setVisible(True)
        self.adduserframe.setVisible(False)
        self.settingsframe.setVisible(False)
        self.feedbackframe.setVisible(False)

    def showAddUser(self):
        self.dashboardframe.setVisible(False)
        self.resultsframe.setVisible(False)
        self.createframe.setVisible(False)
        self.adduserframe.setVisible(True)
        self.settingsframe.setVisible(False)
        self.feedbackframe.setVisible(False)

    def currentExamsData(self):
        cursor.execute("SELECT srno,name,DATE_FORMAT(date,\"%d-%m-%Y\")AS Date,starttime,endtime,type,dept,totalmarks FROM exams where date >= current_date and date < current_date + interval 1 day")
        result = cursor.fetchall()
        print(result)
        self.currentexams.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.currentexams.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.currentexams.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        cursor.execute("SELECT srno,name,DATE_FORMAT(date,\"%d-%m-%Y\")AS Date,starttime,endtime,type,dept,totalmarks FROM exams where date > current_date")
        result = cursor.fetchall()
        print(result)
        self.upcomingexams.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.upcomingexams.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.upcomingexams.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def startExam(self):
        self.rollNo = self.userrollno.text()
        examwindow = Exam(self.rollNo)
        widgets.addWidget(examwindow)
        widgets.setCurrentIndex(widgets.currentIndex()+1)
        widgets.showFullScreen()
class Exam(QMainWindow,Login):
    def __init__(self,rollNo):
        super(Exam,self).__init__(rollNo)
        loadUi("exam.ui",self)
        self.setWindowTitle("OLES - Online Exam System")
        self.blur()
        self.userrollno_2.setText(rollNo)
        self.setUserInfo()
        self.setQuesNo()

    def blur(self):	
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(40) 
        self.blurlbl.setGraphicsEffect(self.blur_effect)

    def setUserInfo(self):
        sql = "select * from user where rollno = %s"
        values = (self.userrollno_2.text(),)
        cursor.execute(sql,values)
        myresult = cursor.fetchone()
        StoreFilepath = "img/image.jpg"
        with open(StoreFilepath, "wb") as file:
            file.write(myresult[6])
            file.close()
        self.userphoto_2.setPixmap(QPixmap("img/image.jpg"))
        self.username_2.setText(myresult[2])
        self.usertype_2.setText(myresult[5])

    def setQuesNo(self):
        names = ['1','2','3','4','5','6','7','8','9','1','2','3','4','5','6','7','8','9']

        positions = [(i,j) for i in range(1,8) for j in range(1,5)]

        for position, name in zip(positions, names):
            print("position=`{}`, name=`{}`".format(position, name))
            button = QPushButton(name)
            button.setFixedHeight(70)
            button.setFixedWidth(70)
            button.setFont(QFont('', 20))
            #button.setStyleSheet("border-radius:1px;")
            self.gridLayout.addWidget(button, *position)


app = QApplication(sys.argv)
loginwindow = Login('dummy')
widgets = QtWidgets.QStackedWidget()
widgets.addWidget(loginwindow)
widgets.setMinimumWidth(1200)
widgets.setMinimumHeight(800)
widgets.show()
app.exec_()
