
import matplotlib.pyplot as plt

correctedans = 20
wrongans = 10

langs = ['Correct','Wrong']
students = [correctedans,wrongans]


barlist = plt.bar(langs,students)
barlist[0].set_color('r')
barlist[1].set_color('y')
plt.savefig('img\\analysis2.png')
plt.close()


import matplotlib.pyplot as plt1

attemptedans = 25
unattemptedans = 15
langs1 = ['Attempted','Unattempted']
students1 = [attemptedans,unattemptedans]
barlist1 = plt1.bar(langs1,students1)
barlist1[0].set_color('g')
barlist1[1].set_color('b')
plt1.savefig("img\\analysis3.png")
plt1.close()


import matplotlib.pyplot as plt2
correctedans = 1
wrongans = 2
attemptedans = 5
unattemptedans = 7
labels = 'Correct', 'Uncorrect', 'Attempted', 'Unattempted'
sizes = [correctedans, wrongans, attemptedans, unattemptedans]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig1, ax1 = plt2.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt2.savefig("img\\analysis.png")
plt2.close()


import numpy as np
import matplotlib.pyplot as plt3
X = ['Q1', 'Q2', 'Q3', 'Q4']
MARKST = [20, 20, 20, 20]
MARKSO = [10, 10, 15, 10]
X_axis = np.arange(len(X))
plt3.bar(X_axis - 0.2, MARKST, 0.4, label='Marks Total')
plt3.bar(X_axis + 0.2, MARKSO, 0.4, label='Marks Got')
plt3.xticks(X_axis, X)
plt3.xlabel("QUESTIONS")
plt3.ylabel("MARKS")
plt3.title("Analysis of questions answers ")
plt3.savefig("img\\analysis4.png")
plt3.close()


