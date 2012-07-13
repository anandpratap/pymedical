#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from account.models import*
from invoicepdf import*
from dailypdf import*
from tempfile import mkdtemp, mkstemp
from secview import*
from yearlypdf import*
from stockpdf import*
def printinvoice(request, invoiceno):
    __invoice = invoice.objects.get(pk=invoiceno)
    client = Address()
    client.firstname = __invoice.patient.name
    provider = Address()
    provider.firstname = "Anand Medical Store"
    provider.lastname = ""
    provider.address = "Ayushman Hospital"
    provider.city = "Kurawar Mandi"
    provider.zip = "465667"
    provider.phone = "07375244340"
    _invoice = Invoice()
    _invoice.setClient(client)
    _invoice.setProvider(provider)
    _invoice.setTitle("Anand Medical Store")
    _invoice.setVS(__invoice.invoice_no)
    _invoice.setCreator(" ")
    _invoice.date = __invoice.invoice_date
    item_list = []
    for i in __invoice.tab.all():
        batch = i.tab.batch_no
        name = i.tab.tag.medicinetype.name[:3] + " " + i.tab.tag.name + " " + batch
        count = i.nitems
        price = i.tab.printed_price
        item = Item()
        item.name = name
        item.count = int(count)
        item.price = float(price)
        item_list.append(item)
    _invoice.items = item_list

        
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)        
    texfilename = mkstemp(dir=tmp_folder)[1]
    print texfilename
    f = open(texfilename+".pdf", "w")
    f.write(_invoice.getContent())
    _invoice.items = [] 
    f.close()
    del _invoice
    response = HttpResponse(file(texfilename+".pdf").read())
    response['Content-Type'] = 'application/pdf'
    filename = 'Invoice_'+ __invoice.invoice_no + ".pdf"
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response


def printdaily(request):

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
    q = querydate_to_date(request.GET.get('q'))
    _invoice = DailyPdf()
    item_list = []
    _date = dateobject.objects.get(date=q)
    for i in _date.invoice_set.all():
        item = Item()
        item.invoiceno = i.invoice_no
        item.patientname = i.patient.name
        item.nitems = int(i.nmedicine)
        item.paid = float(i.paid)
        item.total = float(i.total)
        item_list.append(item)
    _invoice.sitems = item_list
    item_list = []
    for i in _date.purchase_set.all():
        item = Item()
        item.pharmashop = i.pharmashop
        item.itemname = i.tab.tag.name
        item.batchno = i.tab.batch_no
        item.quantity = i.nitems
        item.rate = i.tab.actual_price
        item.amount = i.nitems*float(i.tab.actual_price)
        item_list.append(item)
    _invoice.pitems = item_list

    _invoice.setClient(client)
    _invoice.setProvider(provider)
    _invoice.setTitle("Anand Medical Store")
    _invoice.setVS("00001")
    _invoice.setCreator(" ")
    _invoice.date = q.ctime().replace("00:00:00 ",'')
 

    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)        
    texfilename = mkstemp(dir=tmp_folder)[1]
    print texfilename
    f = open(texfilename+".pdf", "w")
    f.write(_invoice.getContent())
    _invoice.items = [] 
    f.close()
    del _invoice
    response = HttpResponse(file(texfilename+".pdf").read())
    response['Content-Type'] = 'application/pdf'
    filename = "Daily_Balancesheet_"+q.ctime().replace("00:00:00 ",'')+".pdf"
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response

def printyearly(request):

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
    p = querydate_to_date(request.GET.get('p'))
    q = querydate_to_date(request.GET.get('q'))
    _dates = daterange(p,q)
    _invoice = YearlyPdf()
    item_list = []
    for i in _dates:
        item = Item()
        item.date = properdate(i)
        tmp = dailycps(i)
        item.credit = tmp[0]
        item.purchase = tmp[1]
        item.sale = tmp[2]
        item_list.append(item)
    _invoice.sitems = item_list

    _invoice.setClient(client)
    _invoice.setProvider(provider)
    _invoice.setTitle("Anand Medical Store")
    _invoice.setVS("00001")
    _invoice.setCreator(" ")
    _invoice.fromdate = properdate(p)
    _invoice.todate = properdate(q)
 

    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)        
    texfilename = mkstemp(dir=tmp_folder)[1]
    print texfilename
    f = open(texfilename+".pdf", "w")
    f.write(_invoice.getContent())
    _invoice.items = [] 
    f.close()
    del _invoice
    response = HttpResponse(file(texfilename+".pdf").read())
    response['Content-Type'] = 'application/pdf'
    filename = "Balancesheet_"+p.ctime().replace("00:00:00 ",'') + "_to_"+q.ctime().replace("00:00:00 ",'') +".pdf"
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response


def printstockr(request):
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
    _invoice = StockRPdf()
    if request.COOKIES.has_key( 'demand' ):
        demand = urllib.unquote(request.COOKIES[ 'demand' ])
    demand = demand.split('___')
    counter = 0
    item_list = []
    for i in medicine.objects.order_by('medicinetype__name'):
        if str(i.pk) in demand: 
            tmp_tab = i.tablets_set.all()
            count = 0
            for j in tmp_tab:
                count += j.navailable
                tmp_list = j.revision_history.split('&&&')
                pharma_name = ''
                for k in tmp_list[:-1]:
                    try:
                        pharma_name = k.split('___')[2] + ""
                    except:
                        pass
            if count < i.medicinetype.minno:
                counter += 1
                item = Item()
                item.name = i.medicinetype.name[:3] + ". " + i.name 
                item.company = i.medicinefirm.name
                item.pharma = pharma_name
                item_list.append(item)

    
    _invoice.sitems = item_list

    _invoice.setClient(client)
    _invoice.setProvider(provider)
    _invoice.setTitle("Anand Medical Store")
    _invoice.setVS("00001")
    _invoice.setCreator(" ")
    today = datetime.datetime.today()
    _invoice.date = properdate(today)
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)        
    texfilename = mkstemp(dir=tmp_folder)[1]
    print texfilename
    f = open(texfilename+".pdf", "w")
    f.write(_invoice.getContent())
    _invoice.items = [] 
    f.close()
    #del _invoice
    response = HttpResponse(file(texfilename+".pdf").read())
    response['Content-Type'] = 'application/pdf'
    filename = "Stock_Requirements_"+today.ctime().replace("00:00:00",'')+".pdf"
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response

def printstockt(request):
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
    _invoice = StockTPdf()
    item_list = []
    for i in tablets.objects.order_by('tag__name'):
        item = Item()
        item.name = i.tag.name
        item.batchno = i.batch_no
        item.expiry = str(i.expiry_date.month) + "/" +str(i.expiry_date.year) 
        item.rate = float(i.actual_price)
        item.mrp = float(i.printed_price)
        item.na = i.navailable
        item.ns = i.nsold
        item_list.append(item)
       
    _invoice.sitems = item_list

    _invoice.setClient(client)
    _invoice.setProvider(provider)
    _invoice.setTitle("Anand Medical Store")
    _invoice.setVS("00001")
    _invoice.setCreator(" ")
    today = datetime.datetime.today()
    _invoice.date = properdate(today)
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)        
    texfilename = mkstemp(dir=tmp_folder)[1]
    print texfilename
    f = open(texfilename+".pdf", "w")
    f.write(_invoice.getContent())
    _invoice.items = [] 
    f.close()
    #del _invoice
    response = HttpResponse(file(texfilename+".pdf").read())
    response['Content-Type'] = 'application/pdf'
    filename = "Stock_Total_"+today.ctime().replace("00:00:00",'')+".pdf"
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response
