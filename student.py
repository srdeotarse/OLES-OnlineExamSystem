import base64
import io
import sys
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
        self.teacherdashboardframe.setVisible(False)
        self.createframe.setVisible(False)
        self.adduserframe.setVisible(False)
        self.settingsframe.setVisible(False)
        self.feedbackframe.setVisible(False)
        self.adduserbtn.setVisible(False)
        self.createexambtn.setVisible(False)
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
        sql = "insert into {}(quesNo,question,type,option1,option2,option3,option4,option5,marks,correctAns) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(examQuesTablename.lower())
        print(sql)
        value = (quesno,BinaryData,questype,answers[0],answers[1],answers[2],answers[3],answers[4],marks,correctans)        
        cursor.execute(sql,value)
        connection.commit()
        quesno = str(int(quesno)+1)
        self.quesnolbl.setText(quesno)
        self.quesphotolbl.setPixmap(QPixmap())
        self.quesmarkslbl.setText("")
        self.correctanslbl.setText("")
        for i in reversed(range(self.verticalLayoutAns.count())): 
            self.verticalLayoutAns.removeWidget(self.verticalLayoutAns.itemAt(i).widget())

    def exitAddQuesPanel(self):
        self.createframe_2.setVisible(True)
        self.createframe_3.setVisible(True)
        self.addquesframe.setVisible(False)
        self.examtypelbl.setText("")
        self.deptlbl.setText("")
        self.nameofexamlbl.setText("")
        self.totalmarkslbl.setText("")

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
        self.finalstartexambtn.clicked.connect(self.startExam)

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

    def startExam(self):
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.webcam.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(400, 250, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # create socket
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_ip = '192.168.56.1' # paste your server ip address here
        port = 9999
        client_socket.connect((host_ip,port)) # a tuple
        # capture from web cam
        cap = cv2.VideoCapture(0)
        
        # Socket Accept
        while True:            
            while self._run_flag:
                ret, cv_img = cap.read()
                a = pickle.dumps(cv_img)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                # cv2.imshow('TRANSMITTING VIDEO',cv_img)
                # key = cv2.waitKey(1) & 0xFF
                # if key ==ord('q'):
                #     client_socket.close()
                if ret:
                    self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()
        

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

app = QApplication(sys.argv)
loginwindow = Login('dummy')
#applicationwindow = Application('dummy')
widgets = QtWidgets.QStackedWidget()
widgets.addWidget(loginwindow)
widgets.setMinimumWidth(1200)
widgets.setMinimumHeight(800)
widgets.show()
app.exec_()
