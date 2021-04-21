from fpdf import FPDF
pdf = FPDF()
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_font("Arial", size = 12)
# Effective page width, or just epw
epw = pdf.w - 2*pdf.l_margin
pdf.set_font("Arial",'B',16.0) 
pdf.cell(epw, 0.0, 'Result', align='L')
pdf.set_font("Arial", size = 10) 
pdf.ln(3.0)
pdf.cell(100, 10, 'Name - '+self.username.text()+'   Roll No - '+self.userrollno.text(), align='L')
pdf.ln(7.0)
pdf.cell(100, 10, 'Exam ID - '+examid+'    Exam Name - '+examname+'    Exam Type - '+examtype+'   Department - '+department, align='L')
pdf.image('img\logo-oles-filled.png', x = 175, y = 7, w = 20, h = 20)
pdf.ln(5.0)

th = pdf.font_size
col_width = epw/4
# Line break equivalent to 4 lines
pdf.ln(4*th)
 
pdf.set_font('Times','B',14.0) 
pdf.cell(epw, 0.0, 'Attempted Responses', align='C')
pdf.set_font('Times','',10.0) 
pdf.ln(10)

data = [['First name','Last name','Age','City'],
['Jules','Smith',34,'San Juan'],
['Mary','Ramos',45,'Orlando'],[
'Carlson','Banks',19,'Los Angeles']
]
 
# Here we add more padding by passing 2*th as height
for row in data:
    for datum in row:
        # Enter data in colums
        pdf.cell(col_width, 2*th, str(datum), border=1)
 
    pdf.ln(2*th)
        

pdf.output("result.pdf")