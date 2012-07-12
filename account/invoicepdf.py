#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inflect 
import os, datetime
from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics.barcode.qr import QrCodeWidget

from reportlab.graphics.shapes import Drawing

from reportlab.graphics import renderPDF


from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from tempfile import NamedTemporaryFile
from reportlab.graphics.barcode import code39
class Address:
    firstname = ""
    lastname = ""
    address = ""
    city = ""
    zip = ""
    phone = ""
    email = ""
    bank_name = ""
    bank_account = ""
    note = ""
    ic = ""
    dic = ""
 
    def getAddressLines(self):
        lines = [
            "%s %s" % (self.firstname, self.lastname),
            self.address,
            "%s %s" % (self.zip, self.city),
        ]
         
        if self.ic: lines.append("IČ: " + self.ic)
        if self.dic: lines.append("DIČ: " + self.dic)
        return lines
 
    def getContactLines(self):
        return [
            self.phone,
            self.email,
        ]
 
class Item:
    name = ""
    count = 0
    price = 0.0
 
    def total(self):
        return self.count*self.price
 
class Invoice:

    client = Address()
    provider = Address()
    items = []
    title = "Faktura"
    vs = "00000000"
    creator = ""
    sign_image = None
    payment_days = 14
    paytype = "Převodem"
 
    pdffile = None
 
    def __init__(self):
        self.p = inflect.engine()
        self.TIN = "23102404783"
        self.CAN = "20/13/31/2009 21/14/31/2009"
        self.TOP = 260
        self.LEFT = 20
 
        pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'))
 
        self.pdffile = NamedTemporaryFile(delete=False)
         
        self.pdf = Canvas(self.pdffile.name, pagesize = letter)
        self.pdf.setFont("DejaVu", 15)
        self.pdf.setStrokeColorRGB(0, 0, 0)
 
    def __del__(self):
        if os.path.isfile(self.pdffile.name):
            os.unlink(self.pdffile.name)
 
    #############################################################
    ## Setters
    #############################################################
     
    def setClient(self, address):
        self.client = address
 
    def setProvider(self, address):
        self.provider = address
 
    def setTitle(self, value):
        self.title = value
         
    def setVS(self, value):
        self.vs = value
 
    def setCreator(self, value):
        self.creator = value
 
    def setPaytype(self, value):
        self.paytype = value
 
    def setPaymentDays(self, value):
        self.payment_days = int(value)
 
    def addItem(self, item):
        self.items.append(item)
 
    #############################################################
    ## Getters
    #############################################################
 
    def getContent(self):
        # Texty
        self.drawMain()
#        barcode=code39.Extended39("inv"+str(int(self.vs)),barWidth=0.5*mm,barHeight=5*mm)
#        barcode.drawOn(self.pdf,self.TOP+45,(self.LEFT+735))
      
        #qrw =  QrCodeWidget('hello cruel world!')
        #self.pdf.add(qrw)
#        qrw = QrCodeWidget(value = "Invoice" + str(int(self.vs)), barLevel = "Q")
#        b = qrw.getBounds()
#        w=b[2]-b[0]
#        h=b[3]-b[1]
#        qr_size = 60
#        drawing = Drawing(qr_size,qr_size,transform=[float(qr_size)/w,0,0,float(qr_size)/h,0,0])
#        drawing.add(qrw)
        
#        renderPDF.draw(drawing, self.pdf, self.TOP+25, self.LEFT+710)
                        
#        qrw.drawOn(self.pdf,self.TOP+45,(self.LEFT+735))
        self.drawProvider(self.TOP-8,self.LEFT+3)
#        self.drawClient(self.TOP-30,self.LEFT+91)
        self.drawPayment(self.TOP-26,self.LEFT+3)
        self.drawItems(self.TOP-45,self.LEFT)
        self.drawDates(self.TOP-10,self.LEFT+91)
        self.drawWatermark()
        #self.pdf.setFillColorRGB(0, 0, 0)
        self.pdf.showPage()
        self.pdf.save()
 
        f = open(self.pdffile.name)
        data = f.read()
        f.close()
 
        os.unlink(self.pdffile.name)
 
        return data
 
    #############################################################
    ## Draw methods
    #############################################################
 
    def drawMain(self):
        # Horní lajna
        self.pdf.drawString(self.LEFT*mm, self.TOP*mm, self.title)
        self.pdf.drawString((self.LEFT+100)*mm, self.TOP*mm, "Invoice No.: %s" % self.vs)
 
        # Rámečky
        self.pdf.rect((self.LEFT)*mm, (self.TOP-38)*mm, (self.LEFT+156)*mm, 35*mm, stroke=True, fill=False)
 
        path = self.pdf.beginPath()
        path.moveTo((self.LEFT+88)*mm, (self.TOP-3)*mm)
        path.lineTo((self.LEFT+88)*mm, (self.TOP-20)*mm)
        self.pdf.drawPath(path, True, True)
 
        path = self.pdf.beginPath()
        path.moveTo((self.LEFT)*mm, (self.TOP-20)*mm)
        path.lineTo((self.LEFT+88)*mm, (self.TOP-20)*mm)
        self.pdf.drawPath(path, True, True)
 
        path = self.pdf.beginPath()
        path.moveTo((self.LEFT+88)*mm, (self.TOP-26)*mm)
        path.lineTo((self.LEFT+176)*mm, (self.TOP-26)*mm)
        self.pdf.drawPath(path, True, True)
        path = self.pdf.beginPath()
        path.moveTo((self.LEFT+88)*mm, (self.TOP-26)*mm)
        path.lineTo((self.LEFT+88)*mm, (self.TOP-20)*mm)
        self.pdf.drawPath(path, True, True)
    def drawWatermark(self):
        pass
       
    def drawClient(self,TOP,LEFT):
        self.pdf.setFont("DejaVu", 12)
        self.pdf.drawString((LEFT)*mm, (TOP)*mm, "Odběratel")
        self.pdf.setFont("DejaVu", 8)
        text = self.pdf.beginText((LEFT+2)*mm, (TOP-6)*mm)
        text.textLines("\n".join(self.client.getAddressLines()))
        self.pdf.drawText(text)
        text = self.pdf.beginText((LEFT+2)*mm, (TOP-28)*mm)
        text.textLines("\n".join(self.client.getContactLines()))
        self.pdf.drawText(text)
 
    def drawProvider(self,TOP,LEFT):
        LEFT += 90
        self.pdf.setFont("DejaVu", 12)
        self.pdf.drawString((LEFT)*mm, (TOP)*mm, "Address")
        self.pdf.setFont("DejaVu", 9)
        text = self.pdf.beginText((LEFT+2)*mm, (TOP-6)*mm)
        text.textLines("\n".join(self.provider.getAddressLines()))
        self.pdf.drawText(text)
        text = self.pdf.beginText((LEFT+40)*mm, (TOP-6)*mm)
        text.textLines("\n".join(self.provider.getContactLines()))
        self.pdf.drawText(text)
        if self.provider.note:
            self.pdf.drawString((LEFT+2)*mm, (TOP-26)*mm, self.provider.note)
 
    def drawPayment(self,TOP,LEFT):
        self.pdf.setFont("DejaVu", 11)
        self.pdf.drawString((LEFT)*mm, (TOP)*mm, "Patient Name")
        self.pdf.drawString((LEFT+50)*mm, (TOP)*mm, "Date")
        self.pdf.setFont("DejaVu", 9)
        text = self.pdf.beginText((LEFT+50)*mm, (TOP-6)*mm)
        text.textLines(self.date)
        self.pdf.drawText(text)
        
        text = self.pdf.beginText((LEFT+2)*mm, (TOP-6)*mm)
        text.textLines("\n".join(self.client.getAddressLines()))
        self.pdf.drawText(text)
        text = self.pdf.beginText((LEFT+2)*mm, (TOP-28)*mm)
        text.textLines("\n".join(self.client.getContactLines()))
        self.pdf.drawText(text)
 
        self.pdf.drawText(text)
        
    def drawItems(self,TOP,LEFT):
        # Items
        #path = self.pdf.beginPath()
        #path.moveTo((LEFT)*mm, (TOP-4)*mm)
        #path.lineTo((LEFT+176)*mm, (TOP-4)*mm)
        #self.pdf.drawPath(path, True, True)
 
        self.pdf.setFont("DejaVu", 11)
        i=1
        self.pdf.drawString((LEFT+1)*mm, (TOP-i)*mm, "Description")
        self.pdf.drawString((LEFT+98)*mm, (TOP-i)*mm, "Quantity")
        self.pdf.drawString((LEFT+121)*mm, (TOP-i)*mm, "Unit Price")
        self.pdf.drawString((LEFT+149)*mm, (TOP-i)*mm, "Amount")
        i+=7
        self.pdf.setFont("DejaVu", 9)
        # List
        total=0.0

        for x in self.items:
            self.pdf.drawString((LEFT+1)*mm, (TOP-i)*mm, x.name)
            i+=0
            self.pdf.drawString((LEFT+100)*mm, (TOP-i)*mm, "%d" % x.count)
            self.pdf.drawString((LEFT+122)*mm, (TOP-i)*mm, "Rs. %.2f" % x.price)
            self.pdf.drawString((LEFT+150)*mm, (TOP-i)*mm, "Rs. %.2f" % (x.total()))
            i+=5
            total += x.total()
        self.items = []
        path = self.pdf.beginPath()
        path.moveTo((LEFT)*mm, (TOP-i)*mm)
        path.lineTo((LEFT+176)*mm, (TOP-i)*mm)
        self.pdf.drawPath(path, True, True)
        total = round(total,2)
        self.pdf.setFont("DejaVu", 10)
        self.pdf.drawString((LEFT+1)*mm, (TOP-i-8)*mm, self.p.number_to_words(total).title() + " Rupees Only.")
        self.pdf.setFont("DejaVu", 12)
        self.pdf.drawString((LEFT+130)*mm, (TOP-i-8)*mm, "Total: Rs. %s" % total)
        self.pdf.setFont("Helvetica-Bold", 40)
        self.pdf.setStrokeGray(0.25)
        self.pdf.setFillColorRGB(0.95, 0.95, 0.95)
        self.pdf.drawString((LEFT+60)*mm, (TOP-i)*mm, 'PAID')
        self.pdf.setFillColorRGB(0, 0, 0)
      
 
        self.pdf.rect((LEFT)*mm, (TOP-i-12)*mm, (LEFT+156)*mm, (i+19)*mm, stroke=True, fill=False) #140,142
 
        if self.sign_image:
            self.pdf.drawImage(self.sign_image, (LEFT+98)*mm, (TOP-i-72)*mm)
 
        # if self.creator: 
        #     path = self.pdf.beginPath()
        #     path.moveTo((LEFT+110)*mm, (TOP-i-70)*mm)
        #     path.lineTo((LEFT+164)*mm, (TOP-i-70)*mm)
        #     self.pdf.drawPath(path, True, True)
 
        #     self.pdf.drawString((LEFT+112)*mm, (TOP-i-75)*mm, "Authorized Signatory")
 
 
    def drawDates(self,TOP,LEFT):
        LEFT -= 90
        today = datetime.datetime.today()
        payback = today+datetime.timedelta(self.payment_days)
        
        self.pdf.setFont("DejaVu", 10)
        self.pdf.drawString((LEFT)*mm, (TOP+1)*mm, "TIN: %s" % self.TIN)
        self.pdf.drawString((LEFT)*mm, (TOP-4)*mm, "DL: %s" % self.CAN)

 
if __name__ == "__main__":
    client = Address()
    client.firstname = "Anand Singh"
    provider = Address()
    provider.firstname = "Anand Medical Store"
    provider.lastname = ""
    provider.address = "Ayushman Hospital"
    provider.city = "Kurawar Mandi"
    provider.zip = "465667"
    provider.phone = "07375244340"
    #provider.email = "cx@initd.cz"
    #provider.bank_name = "GE Money Bank"
    #provider.bank_account = "181553009/0600"
    #provider.note = "Blablabla"
 
    item1 = Item()
    item1.name = "Crocin "
    item1.count = 10
    item1.price = 122
     
    invoice = Invoice()
    invoice.setClient(client)
    invoice.setProvider(provider)
    invoice.setTitle("Anand Medical Store")
    invoice.setVS("00001")
    invoice.setCreator(" ")
    invoice.addItem(item1)
    invoice.addItem(item1)
    invoice.addItem(item1)
    invoice.addItem(item1)
    invoice.addItem(item1)
    invoice.addItem(item1)
    invoice.addItem(item1)
    invoice.addItem(item1)
    invoice.date = "asdad"
 
    f = open("test.pdf", "w")
    f.write(invoice.getContent())
    f.close()
