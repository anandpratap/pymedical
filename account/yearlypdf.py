#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inflect 
import os, datetime
from reportlab.pdfgen.canvas import Canvas
 
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from tempfile import NamedTemporaryFile
 
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
 
class YearlyPdf:

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
        #self.TIN = "123121414"
        #self.CAN = "13123123123"
        self.TIN = "23102404783"
        self.CAN = "20/13/31/2009 21/14/31/2009"

        self.TOP = 260
        self.LEFT = 20
 
        pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'))
 
        self.pdffile = NamedTemporaryFile(delete=False)
         
        self.pdf = Canvas(self.pdffile.name, pagesize = A4)
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
        self.drawProvider(self.TOP-8,self.LEFT+3)
        #        self.drawClient(self.TOP-30,self.LEFT+91)
        #self.drawPayment(self.TOP-26,self.LEFT+3)
        self.pdf.setFont("DejaVu", 18)

        self.drawDates(self.TOP-10,self.LEFT+91)
        p = self.drawsItems(self.TOP-35,self.LEFT)

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
        self.pdf.drawString((self.LEFT+65)*mm, self.TOP*mm, "Balace Sheet")
        self.pdf.setFont("DejaVu", 8)
        self.pdf.drawString((self.LEFT+120)*mm, (self.TOP)*mm, "Dated to: %s" % self.todate)
        self.pdf.drawString((self.LEFT+120)*mm, (self.TOP+3)*mm, "Dated from: %s" % self.fromdate)

 
        # Rámečky
        #self.pdf.rect((self.LEFT)*mm, (self.TOP-38)*mm, (self.LEFT+156)*mm, 35*mm, stroke=True, fill=False)
 
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
        
    def drawsItems(self,TOP,LEFT):
        LEFT += 10
        # Items
        #path = self.pdf.beginPath()
        #path.moveTo((LEFT)*mm, (TOP-4)*mm)
        #path.lineTo((LEFT+176)*mm, (TOP-4)*mm)
        #self.pdf.drawPath(path, True, True)
        
        self.pdf.setFont("DejaVu", 11)
        i=1
        self.pdf.drawString((LEFT+1)*mm, (TOP-i)*mm, "Date")
        self.pdf.drawString((LEFT+40)*mm, (TOP-i)*mm, "Sale")
        self.pdf.drawString((LEFT+75)*mm, (TOP-i)*mm, "Purchase")
        self.pdf.drawString((LEFT+120)*mm, (TOP-i)*mm, "Credit")
        i+= 2
        path = self.pdf.beginPath()
        path.moveTo((LEFT)*mm, (TOP-i)*mm)
        path.lineTo((LEFT+160)*mm, (TOP-i)*mm)
        self.pdf.drawPath(path, True, True)

        i+=7
        self.pdf.setFont("DejaVu", 9)
        # List
        purchase = 0.0
        sale = 0.0
        credit = 0.0
        for x in self.sitems:
            if TOP - i < 30:
                self.pdf.showPage()
                self.pdf.setFont("DejaVu", 9)
                i = TOP - 270
            self.pdf.drawString((LEFT+1)*mm, (TOP-i)*mm, x.date)
            i+=0
            self.pdf.drawString((LEFT+41)*mm, (TOP-i)*mm,"Rs. " + str(x.sale))
            self.pdf.drawString((LEFT+76)*mm, (TOP-i)*mm,"Rs. " + str(x.purchase))
            self.pdf.drawString((LEFT+121)*mm, (TOP-i)*mm,"Rs. " +str(x.credit))
            
            i+=5
            purchase += x.purchase
            sale += x.sale
            credit += x.credit
            
        path = self.pdf.beginPath()
        path.moveTo((LEFT)*mm, (TOP-i)*mm)
        path.lineTo((LEFT+160)*mm, (TOP-i)*mm)
        self.pdf.drawPath(path, True, True)
        i+= 10
        path = self.pdf.beginPath()
        path.moveTo((LEFT)*mm, (TOP-i)*mm)
        path.lineTo((LEFT+160)*mm, (TOP-i)*mm)
        self.pdf.drawPath(path, True, True)

        sale = round(sale,2)
        purchase = round(purchase,2)
        credit = round(credit,2)
        
        self.pdf.setFont("DejaVu", 10)
        self.pdf.setFont("DejaVu", 11)
        self.pdf.drawString((LEFT+2)*mm, (TOP-i+3)*mm, "Total Sale: ")
        self.pdf.drawString((LEFT+25)*mm, (TOP-i+3)*mm, "Rs. " + str(sale))
        self.pdf.drawString((LEFT+52)*mm, (TOP-i+3)*mm, "Purchase: ")
        self.pdf.drawString((LEFT+73)*mm, (TOP-i+3)*mm, "Rs. " + str(purchase))
        self.pdf.drawString((LEFT+97)*mm, (TOP-i+3)*mm, "Credit: ")
        self.pdf.drawString((LEFT+112)*mm, (TOP-i+3)*mm, "Rs. " + str(credit))

      
 
#        self.pdf.rect((LEFT)*mm, (TOP-i-12)*mm, (LEFT+156)*mm, (i+19)*mm, stroke=True, fill=False) #140,142
        
        if self.sign_image:
            self.pdf.drawImage(self.sign_image, (LEFT+98)*mm, (TOP-i-72)*mm)
        return TOP - i
            # if self.creator: 
        #     path = self.pdf.beginPath()
        #     path.moveTo((LEFT+110)*mm, (TOP-i-70)*mm)
        #     path.lineTo((LEFT+164)*mm, (TOP-i-70)*mm)
        #     self.pdf.drawPath(path, True, True)
 
        #     self.pdf.drawString((LEFT+112)*mm, (TOP-i-75)*mm, "Authorized Signatory")
 
#        self.pdf.rect((LEFT)*mm, (TOP-i-12)*mm, (LEFT+156)*mm, (i+19)*mm, stroke=True, fill=False) #140,142
 
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
    item1.date = "000000111 "
    item1.sale = 1232.0
    item1.purchase = 142.0
    item1.credit = 563.0

    

    
    invoice = YearlyPdf()
    invoice.setClient(client)
    invoice.setProvider(provider)
    invoice.setTitle("Anand Medical Store")
    invoice.setVS("00001")
    invoice.setCreator(" ")
    item_list = []
    for i in range(40):
        item_list.append(item1)
    invoice.sitems = item_list
    
    
    invoice.fromdate = "asdad"
    invoice.todate = "asdad"
 
    f = open("test.pdf", "w")
    f.write(invoice.getContent())
    f.close()
