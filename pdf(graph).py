# def printResult(self):      
#         rows = sorted(set(index.row() for index in self.resultexams.selectedIndexes()))
#         examid = ""
#         examname = ""
#         examtype = ""
#         department = ""
#         for row in rows:
#             examid = self.resultexams.model().data(self.resultexams.model().index(row, 0))
#             examname = self.resultexams.model().data(self.resultexams.model().index(row, 1))
#             examtype = self.resultexams.model().data(self.resultexams.model().index(row, 5))
#             department = self.resultexams.model().data(self.resultexams.model().index(row, 6))
#         sql = "SELECT * FROM {}".format(examid+examname+examtype+department)
#         print("examtable -",examid+examname+examtype+department)
#         cursor.execute(sql)
#         quesans = cursor.fetchall()

#         pdf = FPDF()
#         pdf = FPDF(orientation='P', unit='mm', format='A4')
#         pdf.add_page()
#         pdf.set_font("Arial", size = 12)
#         # Effective page width, or just epw
#         epw = pdf.w - 2*pdf.l_margin
#         pdf.set_font("Arial",'B',16.0) 
#         pdf.cell(epw, 0.0, 'Result', align='L')
#         pdf.set_font("Arial", size = 10) 
#         pdf.ln(3.0)
#         pdf.cell(100, 10, 'Name - '+'Shivam Deotarse'+'   Roll No - '+'5019114', align='L')
#         pdf.ln(7.0)
#         pdf.cell(100, 10, 'Exam ID - '+'19'+'    Exam Name - '+'AT'+'    Exam Type - '+'IA2'+'   Department - '+'IT', align='L')
#         pdf.image('img\logo-oles-filled.png', x = 175, y = 7, w = 20, h = 20)
#         pdf.ln(5.0)

#         th = pdf.font_size
#         # Line break equivalent to 4 lines
#         pdf.ln(4*th)
        
#         pdf.set_font('Times','B',14.0) 
#         pdf.cell(epw, 0.0, 'Attempted Responses', align='C')
#         pdf.set_font('Times','',10.0) 
#         pdf.ln(10)

#         pdf.set_font('Times','B',9.0)
#         pdf.cell(epw/36, 2*th, 'No', border=1, align='C')
#         pdf.cell(epw/1.5, 2*th, 'Question', border=1, align='C')
#         pdf.cell(epw/18, 2*th, 'Type', border=1, align='C')    
#         pdf.cell(epw/10, 2*th, 'Correct Ans', border=1, align='C')
#         pdf.cell(epw/10, 2*th, 'Response', border=1, align='C')
#         pdf.cell(epw/20, 2*th, 'Marks', border=1, align='C')
#         pdf.ln(2*th)

#         pdf.set_font('Times','',10.0)
#         marks = 0
#         attemptedans = 0
#         correctedans = 0
#         wrongans = 0
#         unattemptedans = 0
#         # Here we add more padding by passing 2*th as height
#         for row,row_data in enumerate(quesans):
#             # Enter data in colums
#             pdf.cell(epw/36, 7*th, str(quesans[row][0]), border=1)  
#             sql = "select question from {} where quesno = {}".format(examid+examname+examtype+department, str(quesans[row][0]))
#             cursor.execute(sql)
#             myresult = cursor.fetchone()[0]
#             StoreFilepath = "img/question{}.png".format(str(quesans[row][0]))
#             with open(StoreFilepath, "wb") as file:
#                 file.write(myresult)
#                 file.close() 
#             pdf.cell(epw/1.5, 7*th, '', border=1)     
#             pdf.image('img\question'+str(row+1)+'.jpg', x = 17, y = 58+(row*52), w = 125, h = 20)        
#             pdf.cell(epw/18, 7*th, str(quesans[row][3]), border=1)    
#             correctoptions = quesans[row][10].split("#")
#             correctans = ""
#             for option in correctoptions:
#                 if option==quesans[row][4]:
#                     correctans += "A"+","
#                 if option==quesans[row][5]:
#                     correctans += "B"+","
#                 if option==quesans[row][6]:
#                     correctans += "C"+","
#                 if option==quesans[row][7]:
#                     correctans += "D"+","
#                 if option==quesans[row][8]:
#                     correctans += "E"+","
#             pdf.cell(epw/10, 7*th, correctans, border=1)
#             markedoptions = quesans[row][11].split("#")
#             markedans = ""
#             for option in markedoptions:
#                 if option==quesans[row][4]:
#                     markedans += "A"+","
#                 if option==quesans[row][5]:
#                     markedans += "B"+","
#                 if option==quesans[row][6]:
#                     markedans += "C"+","
#                 if option==quesans[row][7]:
#                     markedans += "D"+","
#                 if option==quesans[row][8]:
#                     markedans += "E"+","
#             pdf.cell(epw/10, 7*th, markedans, border=1)
#             pdf.cell(epw/20, 7*th, str(quesans[row][9]), border=1)
#             pdf.ln(7*th)
#             if quesans[row][4]:
#                 pdf.cell(epw, 1.5*th, "A) "+str(quesans[row][4]), border=1) 
#             pdf.ln(1.5*th)
#             if quesans[row][5]:
#                 pdf.cell(epw, 1.5*th, "B) "+str(quesans[row][5]), border=1) 
#             pdf.ln(1.5*th)
#             if quesans[row][6]:
#                 pdf.cell(epw, 1.5*th, "C) "+str(quesans[row][6]), border=1) 
#             pdf.ln(1.5*th)
#             if quesans[row][7]:
#                 pdf.cell(epw, 1.5*th, "D) "+str(quesans[row][7]), border=1) 
#             pdf.ln(1.5*th)
#             if quesans[row][8]:
#                 pdf.cell(epw, 1.5*th, "E) "+str(quesans[row][8]), border=1) 
#             pdf.ln(1.5*th) 
             

#             #Result Calculation
#             if correctans==markedans:
#                 marks += int(quesans[row][9])
#                 correctedans += 1
#             if correctans!=markedans and markedans:
#                 wrongans +=1
#             if markedans:
#                 attemptedans += 1
#             else : unattemptedans += 1
            
#         pdf.set_font('Times','B',10.0)
#         pdf.cell(epw/5, 1.5*th, "Total marks - "+str(marks), border=1)
#         pdf.cell(epw/5, 1.5*th, "Correct ans - "+str(correctedans), border=1)
#         pdf.cell(epw/5, 1.5*th, "Wrong ans - "+str(wrongans), border=1)
#         pdf.cell(epw/5, 1.5*th, "Attempted ans - "+str(attemptedans), border=1)
#         pdf.cell(epw/5, 1.5*th, "Unattempted ans - "+str(unattemptedans), border=1)
#         pdf.ln(20)        
#         pdf.set_font('Times','B',14.0) 
#         pdf.cell(epw, 0.0, 'Analysis', align='C')
#         pdf.set_font('Times','',10.0) 
#         pdf.ln(10)
        
        # fig = plt.figure()
        # ax = fig.add_axes([0,0,1,1])
        # langs = ['Correct Answers', 'Wrong Answers', 'Unattempted Answers']
        # students = [23,17,35]
        # ax.bar(langs,students)
        # plt.savefig("img/analysis1.png")

        # pdf.image('img\analysis1.png', x = 19, y = 300, w = 125, h = 125)
       
        
#graph 1

import matplotlib.pyplot as plt 
from fpdf import FPDF
        
correctedans = 1  # variables can be taken from above function
wrongans = 2
attemptedans = 5
unattemptedans = 7



labels = 'Correct', 'Uncorrect', 'Attempted', 'Unattempted'
sizes = [correctedans, wrongans, attemptedans, unattemptedans]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.savefig("img/analysis1.png")

#graph2
import matplotlib.pyplot as plt1
correctedans = 20
wrongans = 10 

langs = ['Correct','Wrong']
students = [correctedans,wrongans]


barlist1 = plt1.bar(langs,students)
barlist1[0].set_color('r')
barlist1[1].set_color('y')
plt1.savefig("img/analysis2.png")





#graph3
import matplotlib.pyplot as plt2
attemptedans = 25
unattemptedans = 15



langs1 = ['Attempted','Unattempted']
students1 = [attemptedans,unattemptedans]


barlist = plt2.bar(langs1,students1)
barlist[0].set_color('g')
barlist[1].set_color('b')
plt2.savefig("img/analysis3.png")

 
#pdf.output("result.pdf")


