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




def properdate(_date):
    if _date.day < 10:
        sday = "0" + str(_date.day)
    else:
        sday = str(_date.day)
    if _date.month < 10:
        smonth = "0" + str(_date.month)
    else:
        smonth = str(_date.month)
    syear = str(_date.year)
    return sday + "/" + smonth + "/" + syear



def querydate_to_date(querydate):
    q = querydate.split('-')
    return datetime.date(day=int(q[2]),month=int(q[1]),year=int(q[0]))

def ctime_to_date(ctime):
    _date = ctime.split(' ')
    
    smon = _date[1]
    sday = _date[2]
    syear = _date[4]
    if sday == '':
        sday = _date[3]
        syear = _date[5]
    _month = time.strptime(smon, '%b').tm_mon
    
    return datetime.date(day=int(sday), month=int(_month), year=int(syear))


def invoicedate_to_date(invoicedate):
        _date = invoicedate
        _date = _date.replace(" ",'')
        _year = _date.split(',')[1]
        _day = _date.split(',')[0][-2:]
        _month = time.strptime(_date.split(',')[0].replace(_day,'')[:3], '%b').tm_mon
        return datetime.date(day=int(_day), month=int(_month), year=int(_year))
    
def matchdate(a, b):
    is_match = False
    if a.year == b.year:
        if a.month == b.month:
            if a.day == b.day:
                is_match = True
    return is_match


def dailycps(date):
    #return [credit, purchase, sale]
    purchase = 0.0
    sale = 0.0
    credit = 0.0
    #calc purchase
        
    for i in tablets.objects.all():
        for j in i.revision_history.split("&&&")[:-1]:
            _date = time.strptime(j.split('___')[1])
            _date = datetime.datetime(*_date[0:6])
            if matchdate(_date, date):
                purchase += float(j.split('___')[0])*float(i.actual_price)
    match_found = False
    for i in invoice.objects.order_by('invoice_date'):
        _date = invoicedate_to_date(i.invoice_date)
        if matchdate(_date, date):
            match_found = True
            sale += float(i.total)
            credit += float(i.total) - float(i.paid)
        else:
            if match_found == True:
                break
    return [credit, purchase, sale]

def get_firm_list():
    tmp = "<select name='query' id='ffield' width='10' >"
    for i in medicinefirm.objects.order_by('name'):
        tmp += "<option value="+str(i.pk)+">"+ i.name + '</option>'
    
    tmp += "</select>"
    
    
    return tmp

def statistics(request):
    dailystats = dailycps(datetime.datetime.now())
    firmlist = get_firm_list()
    return render_to_response('stats.html',{'dailystats':dailystats,'firmlist':firmlist})

def send_daily_account( request ):
    if request.is_ajax():
        q = request.GET.get('q')
        _date = querydate_to_date(q)
        results = dailycps(_date)
        return render_to_response( 'daily_account.html', { 'results': results, }) 

def send_monthly_account(request):
    if request.is_ajax():
        q = request.GET.get('q')
        _date = querydate_to_date(q)
        year = _date.year
        month = _date.month
        ndays = calendar.monthrange(year,month)[1]
        results = [0, 0, 0]
        for i in range(ndays):
            _date = datetime.date(day=i+1, month=month, year=year)
            for j in range(3):
                results[j] += dailycps(_date)[j]
        return render_to_response( 'daily_account.html', { 'results': results, }) 
    


def daterange(start_date, end_date):
    tmp = []
    for n in range((end_date - start_date).days+1):
        tmp.append(start_date + datetime.timedelta(n))
    return tmp



def firmstats(request):
    if request.is_ajax():
        q = request.GET.get('q')
        med = medicinefirm.objects.get(pk=int(q)).medicine_set.all()
        
      
        avail = 0.0
        sold = 0.0
        purc = 0.0
        for i in med:
            tab = i.tablets_set.all()
            for j in tab:
                avail += float(j.navailable)*float(j.actual_price)
                purc += (float(j.navailable)+float(j.nsold))*float(j.actual_price)
                sold += float(j.nsold)*float(j.printed_price)
                


        results = [avail, purc, sold]
        return render_to_response( 'firmstats.html', { 'results': results, }) 

