# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.files import File
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
#App import                                                                     
from models import tablets, invoice, pharmashop, stockform, medicine, medicinefirm, medicinetype, medicineform, medicinetypeform, medicinefirmform, pharmaform
import settings
import time
#python import                                                                  
import datetime
import os, sys
import urllib
from views import *
#from latex import LatexDocument
import os
from subprocess import call
from tempfile import mkdtemp, mkstemp
from django.template.loader import render_to_string
import calendar
from secview import*


def generate_spplot_array():
    start_date = datetime.datetime(day = 28, month=6, year=2012) 
    end_date = datetime.datetime.now()
    _dates = daterange(start_date, end_date)
    tmp_s = '['
    tmp_p = '['
    for i in _dates:
        tmp_s += "[Date.UTC("+str(i.year)+","+str(i.month-1)+","+ str(i.day)+"),"+ str(dailycps(i)[2])+"]" + ','
        tmp_p += "[Date.UTC("+str(i.year)+","+str(i.month-1)+","+ str(i.day)+"),"+ str(dailycps(i)[1])+"]" + ','
    tmp_s += ']'
    tmp_p += ']'
    return [tmp_p, tmp_s]


def cdata(id, name, value, tablist, tabvalue):
    tmp = ''
    tmp += "{y:" + str(value) + ", color: colors[" + str(id) + "],drilldown:{ name:'"+name+"',categories: ["
    for i in range(len(tablist)):
        tmp += "'" +tablist[i]+ "'"
        tmp += ","
    tmp += "],data: ["
    for i in range(len(tablist)):
        tmp += str(tabvalue[i])
        tmp += ","
    tmp += "], color: colors[" + str(id) + "]}}"
    return tmp
    
def generate_cplot_array():
    tsale = profit_calculator()[0]
    tpurchase = profit_calculator()[1]
    tmp = ''
    count = 0
    tmp_1 = '['
    for i in medicinefirm.objects.all():
     
        tablist = []
        tabvalue = []
        med = i.medicine_set.all()
        name = i.name
        sale = 0.0
        for j in med:
            tab = j.tablets_set.all()
            med_s = 0.0
            for k in tab:
                sale += float(k.printed_price)*int(k.nsold)
                med_s += float(k.printed_price)*int(k.nsold)
            tablist.append(j.name)
            tabvalue.append(med_s/10000.0)
        if sale/tsale*100 > 2:
            tmp += cdata(count, name, sale/tsale*100, tablist=[], tabvalue=[]) + ","
            tmp_1 += "'" +  i.name + "'" + ","
            count += 1
    tmp_1 += "]"
    return tmp, tmp_1
def writetofile():
    tmp_str = generate_spplot_array()
    _file = open("/home/maverick/Dropbox/medical/template/static/purchase.txt", "w+")
    _file.writelines(tmp_str[0])
    _file.close()
    _file = open("/home/maverick/Dropbox/medical/template/static/sale.txt", "w+")
    _file.writelines(tmp_str[1])
    _file.close()
    return 0



def plots(request):
    tmp_str = generate_spplot_array()
    return render_to_response('plots.html',{'string':tmp_str})
