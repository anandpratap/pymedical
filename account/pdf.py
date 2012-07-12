#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from account.models import*
from invoicepdf import*
from tempfile import mkdtemp, mkstemp
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
