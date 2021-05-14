import base64
import io
import sys
import os
import threading
import mysql.connector
from mysql.connector import Error
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import socket,cv2, pickle,struct
import numpy as np
#import face_recognition
import time
from datetime import datetime,date
from gaze_tracking import GazeTracking
import keyboard
import random
from fpdf import FPDF
#import matplotlib.pyplot as plt

connection = mysql.connector.connect(host='localhost', database='OnlineExamSystem', user='root', password='', port='3306')
cursor = connection.cursor(buffered=True)
msgtostudent = ""
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
            self.label_3.setText("Login failed")

    def createAccount(self):
        self.loginframe.setVisible(False)
        self.signframe.setVisible(True)
        self.label_2.setText("")

    def loginAccount(self):
        self.signframe.setVisible(False)
        self.loginframe.setVisible(True)
        self.label_3.setText("")
        
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

        if self.rollno_3.text():
            with open (self.rollno_3.text(),"rb") as File:
                BinaryData = File.read()
            sql = "insert into user (rollno,name,email,type,password,photo) values (%s,%s,%s,%s,%s,%s)"
            value = (rollno,name,email,type,password,BinaryData)  

        if (rollno.isdigit() == False):
           self.label_2.setText("Please Enter a Roll Number in Digits")

        elif (len(rollno) < 7):
            self.label_2.setText("Please Enter a Roll Number of Length 7 Digits")

        elif (len(password)<8):
            self.label_2.setText("Please Enter a Strong Password")

        elif (confirmPass != password):
            self.label_2.setText("Please Enter Correct Password")

        elif (name == '' or email == '' or password == '' or rollno == '' or self.rollno_3.text() == ''):
            self.label_2.setText("Please fill all the data")

        else:
            cursor.execute(sql,value)
            connection.commit()
            self.label_2.setText("Account created successfully")
            self.name.setText("")
            self.rollno_2.setText("")
            self.email.setText("")
            self.password_2.setText("")
            self.password_3.setText("") 


class Application(QMainWindow,Login):
    def __init__(self,rollNo):
        super(Application,self).__init__(rollNo)
        loadUi("application.ui",self)
        self.setWindowTitle("OLES - Online Exam System")
        self.blur()
        self.userrollno.setText(rollNo)
        self.setUserInfo()
        self.resultsframe.setVisible(False)
        self.teacherdashboardframe.setVisible(False)
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
        self.createnewexambtn.clicked.connect(self.createNewExam)   
        self.refreshbtn.clicked.connect(self.setCreatedExams) 
        self.addquesframe.setVisible(False)
        self.addquesbtn.clicked.connect(self.showAddQuesPanel)
        self.startproctoringbtn.clicked.connect(self.startProctoring)
        self.endproctoringbtn.clicked.connect(self.endProctoring)
        self.sendmsgbtn.clicked.connect(self.sendMsgFromTeacher)
        self.endexambtn.clicked.connect(self.endStudentExam)
        self.photobutton.clicked.connect(self.getphoto)
        self.submitbtn.clicked.connect(self.adduser)
        self.existinguserbtn.clicked.connect(self.showAddedUsers)
        self.getSubjResponsesbtn.clicked.connect(self.showSubjQues)
        self.refreshResultsbtn.clicked.connect(self.showResultsTable)
        self.rollno_10.setVisible(False)

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
        if myresult :
            with open(StoreFilepath, "wb") as file:
                file.write(myresult[6])
                file.close()
            self.userphoto.setPixmap(QPixmap("img/image.jpg"))
            self.username.setText(myresult[2])
            self.usertype.setText(myresult[4])

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
        self.printresultbtn.setVisible(False)
        self.resultexams.setVisible(False)

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
        self.setCreatedExams()

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
        self.currentexams.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.currentexams.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.currentexams.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.currentexams.setSelectionBehavior(QTableView.SelectRows);


        cursor.execute("SELECT srno,name,DATE_FORMAT(date,\"%d-%m-%Y\")AS Date,starttime,endtime,type,dept,totalmarks FROM exams where date > current_date")
        result = cursor.fetchall()
        self.upcomingexams.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.upcomingexams.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.upcomingexams.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.upcomingexams.setSelectionBehavior(QTableView.SelectRows);


    def startExam(self):
        self.rollNo = self.userrollno.text()
        examwindow = Exam(self.rollNo)
        widgets.addWidget(examwindow)
        widgets.setCurrentIndex(widgets.currentIndex()+1)
        widgets.showFullScreen()

        # rows = sorted(set(index.row() for index in self.currentexams.selectedIndexes()))
        # for row in rows:
        #     self.examQuesTablename = (self.createdexams.model().data(self.createdexams.model().index(row, 0)),self.createdexams.model().data(self.createdexams.model().index(row, 1)),self.createdexams.model().data(self.createdexams.model().index(row, 5)),self.createdexams.model().data(self.createdexams.model().index(row, 6)))

    def startProctoring(self):
        self.teacherdashboardframe.setVisible(True)
        self.dashboardframe.setVisible(False)
        
        #  # create the video capture thread
        # self.thread = VideoThread()
        # # connect its signal to the update_image slot
        # self.thread.change_pixmap_signal.connect(self.update_image)
        # # start the thread
        # self.thread.start()     
        receive = self.start()

    def sendMsgFromTeacher(self):
        global msgtostudent
        msgtostudent = self.msgstudent.text()
        print("Message form teacher to student - ",msgtostudent)
        self.msgstudent.setText("")

    def msgToStudent(self):
        global msgtostudent
        return msgtostudent        

    def start(self):
        """
        Establishes the client-server connection. Gathers user input for the username,
        creates and starts the Send and Receive threads, and notifies other connected clients.

        Returns:
            A Receive object representing the receiving thread.
        """
        """
        Initializes and runs the GUI application.

        Args:
            host (str): The IP address of the server's listening socket.
            port (int): The port number of the server's listening socket.
        """
        host_name  = socket.gethostname()
        host = socket.gethostbyname(host_name)
        port = 1060
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        name = self.username.text()
        messages = None
        print('Trying to connect to {}:{}...'.format(host, port))
        sock.connect((host, port))
        print('Successfully connected to {}:{}'.format(host, port))
        
        # print()
        # self.name = input('Your name: ')

        # print()
        # print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

        # Create send and receive threads
        send = Send(sock, name)
        receive = Receive(sock, name)
        receive.change_pixmap_signal.connect(self.update_image)
        # Start send and receive threads
        send.start()
        receive.start()

        #sock.sendall(bytes("Server: {} has joined the chat. Say hi!".format(name),'utf-8'))
        print("\rAll set! Leave the chatroom anytime by typing 'QUIT'\n")
        print('{}: '.format(name), end = '')

        return receive

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        #print("Teacher update image running")
        qt_img = self.convert_cv_qt(cv_img)
        self.student1lbl.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(400, 250, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p) 

    def endStudentExam(self):
        global msgtostudent
        msgtostudent="endexam"

    def endProctoring(self):
        global msgtostudent
        msgtostudent="QUIT"
        self.teacherdashboardframe.setVisible(False)
        self.dashboardframe.setVisible(True)


    def createNewExam(self):
        examname = self.nameofexamlbl.text()
        examtype = self.examtypelbl.text()
        totalmarks = self.totalmarkslbl.text()
        examdate = self.dateEdit.date().toString(Qt.ISODate)
        starttime = self.timeEdit.time().toString(Qt.ISODate)
        endtime = self.timeEdit_2.time().toString(Qt.ISODate)
        department = self.deptlbl.text()

        print("date- ",examdate)
        print("starttime- ",starttime)
        print("endtime- ",endtime)

        sql = "insert into exams(name,date,starttime,endtime,type,totalmarks,dept) values(%s,%s,%s,%s,%s,%s,%s)"
        values =(examname,examdate,starttime,endtime,examtype,totalmarks,department)
        cursor.execute(sql,values)

        sql1 = "select srno from exams where name = %s and date = %s and starttime = %s and endtime = %s and type = %s and totalmarks = %s and dept = %s"
        values1 =(examname,examdate,starttime,endtime,examtype,totalmarks,department)
        cursor.execute(sql1,values1)
        myresult = cursor.fetchone()

        examQuesTablename = str(myresult[0])+examname+examtype+department;
        sql2 = "CREATE TABLE {} ( `quesNo` VARCHAR(20) NOT NULL ,`shuffledNo` VARCHAR(20) NULL , `question` LONGBLOB NOT NULL , `type` VARCHAR(255) NOT NULL , `option1` VARCHAR(255) NULL , `option2` VARCHAR(255) NULL , `option3` VARCHAR(255) NULL , `option4` VARCHAR(255) NULL , `option5` VARCHAR(255) NULL ,`marks` VARCHAR(20) NOT NULL , `correctAns` VARCHAR(255) NOT NULL , PRIMARY KEY (`quesNo`))".format(examQuesTablename)
        cursor.execute(sql2)
        self.createexamstatuslbl.setText("New exam created.")

    def setCreatedExams(self):
        cursor.execute("SELECT srno,name,DATE_FORMAT(date,\"%d-%m-%Y\")AS Date,starttime,endtime,type,dept,totalmarks FROM exams ")
        result = cursor.fetchall()
        self.createdexams.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.createdexams.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.createdexams.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.createdexams.setSelectionBehavior(QTableView.SelectRows);
        self.createdexams.clicked.connect(self.selectCreatedExam)
        self.createexamstatuslbl.setText("")
        self.nameofexamlbl.setText("")
        self.examtypelbl.setText("")
        self.totalmarkslbl.setText("")        
        self.deptlbl.setText("")

    def selectCreatedExam(self):
        rows = sorted(set(index.row() for index in self.createdexams.selectedIndexes()))
        for row in rows:
            self.examidlbl.setText(self.createdexams.model().data(self.createdexams.model().index(row, 0)))
            self.examnamelbl.setText(self.createdexams.model().data(self.createdexams.model().index(row, 1)))
            self.examtypelbl_2.setText(self.createdexams.model().data(self.createdexams.model().index(row, 5)))
            self.deptlbl_2.setText(self.createdexams.model().data(self.createdexams.model().index(row, 6)))

    def showAddQuesPanel(self):
        self.createframe_2.setVisible(False)
        self.createframe_3.setVisible(False)
        self.addquesframe.setVisible(True)
        self.quesphotobtn.clicked.connect(self.getquesphoto)
        self.addansbtn.clicked.connect(self.addAnstoCreatedExam)
        self.quesphotoaddresslbl.setVisible(False)
        self.quesconfirmbtn.clicked.connect(self.addQuestoCreatedExam)
        self.addquesexitbtn.clicked.connect(self.exitAddQuesPanel)
        examQuesTablename = self.examidlbl.text()+self.examnamelbl.text()+self.examtypelbl_2.text()+self.deptlbl_2.text()
        sql = "SELECT quesNo FROM {} ORDER BY quesNo DESC LIMIT 1".format(examQuesTablename,)
        cursor.execute(sql)
        quesresult = cursor.fetchall()
        if quesresult:
            print("last ques -",quesresult[0])
            self.quesnolbl.setText(str(int(quesresult[0][0])+1))

    def getquesphoto(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Image files (*.jpg *.png)",options=QFileDialog.DontUseNativeDialog)
        self.quesphotolbl.setPixmap(QPixmap(fname))
        self.quesphotoaddresslbl.setText(fname)

    def addAnstoCreatedExam(self):
        lineedit = QLineEdit()
        lineedit.setFixedHeight(50)
        lineedit.setFixedWidth(780)
        lineedit.setFont(QFont('', 14))
        lineedit.setStyleSheet("background: rgba(255,255,255,0.6); border:none; border-radius:5px;")
        lineedit.setPlaceholderText("      Type your answer")
        self.verticalLayoutAns.addWidget(lineedit) 

    def addQuestoCreatedExam(self):
        examQuesTablename = self.examidlbl.text()+self.examnamelbl.text()+self.examtypelbl_2.text()+self.deptlbl_2.text()       
        quesno = self.quesnolbl.text()
        with open (self.quesphotoaddresslbl.text(),"rb") as File:
            BinaryData = File.read()
        questype = self.questypebox.currentText()
        marks = self.quesmarkslbl.text()
        correctans = self.correctanslbl.text()
        time = self.questimelbl.text()
        widgets = (self.verticalLayoutAns.itemAt(i).widget() for i in range(self.verticalLayoutAns.count())) 
        answers = ()
        for widget in widgets:
            if isinstance(widget, QLineEdit):
                answers = answers + (widget.text(),)
        print("Answers - ",answers)
        if(len(answers)<5):
            for i in range(len(answers),5):
                answers = answers + ("",)
        print("Answers - ",answers)
        sql = "insert into {}(quesNo,question,type,option1,option2,option3,option4,option5,marks,correctAns,time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(examQuesTablename.lower())
        print(sql)
        value = (quesno,BinaryData,questype,answers[0],answers[1],answers[2],answers[3],answers[4],marks,correctans,time)       
        cursor.execute(sql,value)
        connection.commit()
        quesno = str(int(quesno)+1)
        self.quesnolbl.setText(quesno)
        self.quesphotolbl.setPixmap(QPixmap())
        self.quesmarkslbl.setText("")
        self.correctanslbl.setText("")
        self.questimelbl.setText("")
        for i in reversed(range(self.verticalLayoutAns.count())): 
            self.verticalLayoutAns.itemAt(i).widget().deleteLater()

    def exitAddQuesPanel(self):
        self.createframe_2.setVisible(True)
        self.createframe_3.setVisible(True)
        self.addquesframe.setVisible(False)
        self.examtypelbl.setText("")
        self.deptlbl.setText("")
        self.nameofexamlbl.setText("")
        self.totalmarkslbl.setText("")

    def getphoto(self):
        fname1, _ = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)",options=QFileDialog.DontUseNativeDialog)
        self.photo.setPixmap(QPixmap(fname1))
        self.rollno_10.setText(fname1)

    def adduser(self):
        name1 = self.name1.text()
        rollno1 = self.rollno_11.text()
        email1 = self.email1.text()
        password1 = self.password_5.text()
        confirmPass1 = self.password_6.text()
        type1 = self.typeCombo_3.currentText()
        print("hi")

        with open(self.rollno_10.text(), "rb") as File:
            BinaryData1 = File.read()

        sql = "insert into user (rollno,name,email,type,password,photo) values (%s,%s,%s,%s,%s,%s)"
        value = (rollno1, name1, email1, type1, password1, BinaryData1)

        if (rollno1.isdigit() == False):
            self.addnewuserstatuslbl.setText("Please Enter a Roll Number in Digits")

        elif (len(rollno1) < 7):
            self.addnewuserstatuslbl.setText("Please Enter a Roll Number of Length 7 Digits")

        elif (len(password1) < 8):
            self.addnewuserstatuslbl.setText("Please Enter a Strong Password")

        elif (confirmPass1 != password1):
            self.addnewuserstatuslbl.setText("Please Enter Correct Password")

        elif (name1 == '' or email1 == '' or password1 == '' or rollno1 == '' or self.rollno_10.text() == ''):
            self.addnewuserstatuslbl.setText("Please fill all the data")

        else:
            cursor.execute(sql, value)
            connection.commit()
            self.addnewuserstatuslbl.setText("User added.")

    def showAddedUsers(self):
        usertype = '"'+self.typeCombo_4.currentText()+'"'
        cursor.execute("SELECT rollno,name,email,type FROM user where type = {}".format(usertype))
        result = cursor.fetchall()
        self.existingusers.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.existingusers.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.existingusers.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.existingusers.setSelectionBehavior(QTableView.SelectRows)

    def showResultsTable(self):
        cursor.execute("SELECT srno,name,type,dept FROM exams")
        result = cursor.fetchall()
        self.resultexams_2.setRowCount(0)
        for row_number, row_data in enumerate(result):
            sql = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'onlineexamsystem' AND TABLE_NAME = '{}' AND COLUMN_NAME = '{}'".format(str(result[row_number][0])+str(result[row_number][1]).lower()+str(result[row_number][2]).lower()+str(result[row_number][3]).lower(), "pdf"+self.rollnoresultlbl.text())
            cursor.execute(sql)
            existexam = cursor.fetchall()
            if existexam:
                sql1 ="SELECT srno,name,DATE_FORMAT(date,\"%d-%m-%Y\")AS Date,starttime,endtime,type,dept,totalmarks FROM exams where srno = {}".format(str(result[row_number][0]))
                cursor.execute(sql1)
                examdata = cursor.fetchall()
                for row_number, row_data in enumerate(examdata):
                    self.resultexams_2.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.resultexams_2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            connection.commit()
        self.resultexams_2.setSelectionBehavior(QTableView.SelectRows)

    def showSubjQues(self):      
        rows = sorted(set(index.row() for index in self.resultexams_2.selectedIndexes()))
        examid = ""
        examname = ""
        examtype = ""
        department = ""
        for row in rows:
            examid = self.resultexams_2.model().data(self.resultexams_2.model().index(row, 0))
            examname = self.resultexams_2.model().data(self.resultexams_2.model().index(row, 1))
            examtype = self.resultexams_2.model().data(self.resultexams_2.model().index(row, 5))
            department = self.resultexams_2.model().data(self.resultexams_2.model().index(row, 6))
        sql = "SELECT quesNo,pdf{} FROM {} WHERE type = 'subj'".format(self.rollnoresultlbl.text(),examid+examname+examtype+department)
        print("examtable -",examid+examname+examtype+department)
        cursor.execute(sql)
        subjPdf = cursor.fetchall()
        if subjPdf:
            for row_number, row_data in enumerate(subjPdf):
                self.resultexams_3.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.resultexams_3.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.resultexams_3.setSelectionBehavior(QTableView.SelectRows)

    def getSubjPDF(self):
        rows = sorted(set(index.row() for index in self.resultexams_2.selectedIndexes()))
        examid = ""
        examname = ""
        examtype = ""
        department = ""
        for row in rows:
            examid = self.resultexams_2.model().data(self.resultexams_2.model().index(row, 0))
            examname = self.resultexams_2.model().data(self.resultexams_2.model().index(row, 1))
            examtype = self.resultexams_2.model().data(self.resultexams_2.model().index(row, 5))
            department = self.resultexams_2.model().data(self.resultexams_2.model().index(row, 6))
        sql = "UPDATE {} quesNo,pdf{} FROM {} WHERE type = 'subj'".format(self.rollnoresultlbl.text(),examid+examname+examtype+department)


class Exam(QMainWindow,Login):
    def __init__(self,rollNo):
        super(Exam,self).__init__(rollNo)
        loadUi("exam.ui",self)
        self.setWindowTitle("OLES - Online Exam System")
        self.blur()
        self.userrollno_2.setText(rollNo)
        self.setUserInfo()
        self.setQuesNo()
        self.exampanel.setVisible(False)
        self.startexambtn_4.clicked.connect(self.showExamPanel)
        self.setAns()
        #self.finalstartexambtn.clicked.connect(self.startExam)

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
        self.usertype_2.setText(myresult[4])

        #self.examidlbl.setText(examQuesTablename[0])

    def setQuesNo(self):
        sql = ""
        names = ['1','2','3','4','5','6','7','8','9','1','2','3','4','5','6','7','8','9']

        positions = [(i,j) for i in range(1,8) for j in range(1,5)]

        for position, name in zip(positions, names):
            print("position=`{}`, name=`{}`".format(position, name))
            button = QPushButton(name)
            button.setFixedHeight(70)
            button.setFixedWidth(70)
            button.setFont(QFont('', 20))
            # button.setDefault(True)
            button.setStyleSheet("background: rgba(255,255,255,0.75); border:none; border-radius:5px;")
            self.gridLayout.addWidget(button, *position)

    def showExamPanel(self):
        self.exampanel.setVisible(True)
        self.informationframe.setVisible(False)        

    def setAns(self):
        answers = ['abc','efg','hij','lmno']
        for ans in answers:
            label = QLabel(ans)
            label.setFixedWidth(1280)
            label.setFont(QFont('',14))
            label.setStyleSheet("background: rgba(255,255,255,0.6);border-radius:5px;")
            self.verticalLayout.addWidget(label)    

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # Socket Create
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_name  = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print('HOST IP:',host_ip)
        port = 9999
        socket_address = (host_ip,port)

        # Socket Bind
        server_socket.bind(socket_address)

        # Socket Listen
        server_socket.listen(5)
        print("LISTENING AT:",socket_address)

        client_socket,addr = server_socket.accept()
        print('GOT CONNECTION FROM:',addr)

        data = b""
        payload_size = struct.calcsize("Q")        

        while self._run_flag:
            while len(data) < payload_size:
                data+=client_socket.recv(4*1024)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
                
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            cv_img = pickle.loads(frame_data)
            # cv2.imshow("RECEIVING VIDEO",cv_img)
            # key = cv2.waitKey(1) & 0xFF
            # if key  == ord('q'):
            #     break
            self.change_pixmap_signal.emit(cv_img)
        client_socket.close()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
        client_socket.close()


class Send(threading.Thread):
    """
    Sending thread listens for user input from the command line.

    Attributes:
        sock (socket.socket): The connected socket object.
        name (str): The username provided by the user.
    """
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        """
        Listens for user input from the command line only and sends it to the server.
        Typing 'QUIT' will close the connection and exit the application.
        """
        while True:
            #print('{}: '.format(self.name), end='')
            #sys.stdout.flush()
            a = Application("rollno")
            message = a.msgToStudent()           
            global msgtostudent            
            # Type 'QUIT' to leave the chatroom
            print("msgtostudent - ",msgtostudent)
            if msgtostudent == 'QUIT':
                #self.sock.sendall('Server: {} has left the chat.'.format(self.name))
                break            
            # Send message to server for broadcasting
            else:
                self.sock.send(bytes('{}'.format(message),'utf-8'))
                msgtostudent = ""          
                
        
        print('\nQuitting...')
        self.sock.close()
        #os._exit(0)


class Receive(QThread):
    """
    Receiving thread listens for incoming messages from the server.

    Attributes:
        sock (socket.socket): The connected socket object.
        name (str): The username provided by the user.
        messages (tk.Listbox): The tk.Listbox object containing all messages displayed on the GUI.
    """

    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):
        """
        Receives data from the server and displays it in the GUI.
        Always listens for incoming data until either end has closed the socket.
        """

        data = b""
        payload_size = struct.calcsize("Q")
        global msgtostudent
        while(not msgtostudent=="QUIT"):
            #message = self.sock.recv(1024).decode('ascii')            
            while len(data) < payload_size:
                packet = self.sock.recv(1024) # 4K
                if not packet: break
                data+=packet                
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            
            while len(data) < msg_size:
                data += self.sock.recv(1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            cv_img = pickle.loads(frame_data)
            # cv2.imshow("RECEIVING VIDEO",frame) 
            # key = cv2.waitKey(1) & 0xFF
            # if key  == ord('q'):
            #     break
            self.change_pixmap_signal.emit(cv_img)

            # if message:

            #     if self.messages:
            #         self.messages.insert(tk.END, message)
            #         print('hi')
            #         print('\r{}\n{}: '.format(message, self.name), end = '')
                
            #     else:
            #         # Thread has started, but client GUI is not yet ready
            #         print('\r{}\n{}: '.format(message, self.name), end = '')
            
            
        # Server has closed the socket, exit the program
        print('\nOh no, we have lost connection to the server!')
        print('\nQuitting...')
        self.sock.close()
        #os._exit(0)

class Client:
    """
    Supports management of client-server connections and integration with the GUI.

    Attributes:
        host (str): The IP address of the server's listening socket.
        port (int): The port number of the server's listening socket.
        sock (socket.socket): The connected socket object.
        name (str): The username of the client.
        messages (tk.Listbox): The tk.Listbox object containing all messages displayed on the GUI.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None
    
    def start(self):
        """
        Establishes the client-server connection. Gathers user input for the username,
        creates and starts the Send and Receive threads, and notifies other connected clients.

        Returns:
            A Receive object representing the receiving thread.
        """
        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Successfully connected to {}:{}'.format(self.host, self.port))
        
        # print()
        # self.name = input('Your name: ')

        # print()
        # print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

        # Create send and receive threads
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)
        a = Application("1")
        receive.change_pixmap_signal.connect(a.update_image)
        # Start send and receive threads
        send.start()
        receive.start()

        self.sock.sendall(bytes("Server: {} has joined the chat. Say hi!".format(self.name),'utf-8'))
        print("\rAll set! Leave the chatroom anytime by typing 'QUIT'\n")
        print('{}: '.format(self.name), end = '')

        return receive

    # def send(self, text_input):
    #     """
    #     Sends text_input data from the GUI. This method should be bound to text_input and 
    #     any other widgets that activate a similar function e.g. buttons.
    #     Typing 'QUIT' will close the connection and exit the application.

    #     Args:
    #         text_input(tk.Entry): A tk.Entry object meant for user text input.
    #     """
    #     message = text_input.get()
    #     text_input.delete(0, tk.END)
    #     self.messages.insert(tk.END, '{}: {}'.format(self.name, message))

    #     # Type 'QUIT' to leave the chatroom
    #     if message == 'QUIT':
    #         self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
            
    #         print('\nQuitting...')
    #         self.sock.close()
    #         os._exit(0)
        
    #     # Send message to server for broadcasting
    #     else:
    #         self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))


# def main(host, port):
#     """
#     Initializes and runs the GUI application.

#     Args:
#         host (str): The IP address of the server's listening socket.
#         port (int): The port number of the server's listening socket.
#     """
#     client = Client(host, port)
#     receive = client.start()

#     # window = tk.Tk()
#     # window.title('Chatroom')

#     # frm_messages = tk.Frame(master=window)
#     # scrollbar = tk.Scrollbar(master=frm_messages)
#     # messages = tk.Listbox(
#     #     master=frm_messages, 
#     #     yscrollcommand=scrollbar.set
#     # )
#     # scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
#     # messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
#     # client.messages = messages
#     # receive.messages = messages

#     # frm_messages.grid(row=0, column=0, columnspan=2, sticky="nsew")

#     # frm_entry = tk.Frame(master=window)
#     # text_input = tk.Entry(master=frm_entry)
#     # text_input.pack(fill=tk.BOTH, expand=True)
#     # text_input.bind("<Return>", lambda x: client.send(text_input))
#     # text_input.insert(0, "Your message here.")

#     # btn_send = tk.Button(
#     #     master=window,
#     #     text='Send',
#     #     command=lambda: client.send(text_input)
#     # )

#     # frm_entry.grid(row=1, column=0, padx=10, sticky="ew")
#     # btn_send.grid(row=1, column=1, pady=10, sticky="ew")

#     # window.rowconfigure(0, minsize=500, weight=1)
#     # window.rowconfigure(1, minsize=50, weight=0)
#     # window.columnconfigure(0, minsize=500, weight=1)
#     # window.columnconfigure(1, minsize=200, weight=0)

#     # window.mainloop()


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Chatroom Server')
#     parser.add_argument('host', help='Interface the server listens at')
#     parser.add_argument('-p', metavar='PORT', type=int, default=1060,
#                         help='TCP port (default 1060)')
#     args = parser.parse_args()

#     main(args.host, args.p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginwindow = Login('dummy')
    #applicationwindow = Application('dummy')
    widgets = QtWidgets.QStackedWidget()
    widgets.addWidget(loginwindow)
    widgets.setMinimumWidth(1200)
    widgets.setMinimumHeight(800)
    widgets.setWindowTitle("OLES - Online Exam System - Teacher")
    widgets.show()
    app.exec_()
