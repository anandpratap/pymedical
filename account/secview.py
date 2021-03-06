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

def invoiceprofitcalculator(pk):
    i = invoice.objects.get(pk=pk)
    tab = i.tab.all()
    tmp = 0.0
    for j in tab:
        tmp += (float(j.tab.printed_price)-float(j.tab.actual_price))*j.nitems
    return tmp

def dailycps(date):
    #return [credit, purchase, sale]
    purchase = 0.0
    sale = 0.0
    credit = 0.0
    profit = 0.0
    #calc purchase
    try:
        dateob = dateobject.objects.select_related().get(date=date)
        for i in dateob.purchase_set.select_related().all():
            purchase += i.nitems*float(i.tab.actual_price)
        for i in dateob.invoice_set.select_related().all():
            sale += float(i.total)
            credit += float(i.total) - float(i.paid)
            #profit += invoiceprofitcalculator(i.pk)
        for i in dateob.creditobject_set.select_related().all():
            credit -= float(i.amount)
    except:
        pass
        
    return [credit, purchase, sale, profit]

def get_firm_list():
    tmp = "<select name='query' id='ffield' width='10' >"
    for i in medicinefirm.objects.order_by('name'):
        tmp += "<option value="+str(i.pk)+">"+ i.name + '</option>'
    
    tmp += "</select>"
    
    
    return tmp

def statistics(request):
    dailystats = dailycps(datetime.date.today())
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
        results = [0, 0, 0, 0]
        for i in range(ndays):
            _date = datetime.date(day=i+1, month=month, year=year)
            tmp = dailycps(_date)
            for j in range(4):
                results[j] += tmp[j]
        return render_to_response( 'daily_account.html', { 'results': results, }) 
    


def daterange(start_date, end_date):
    tmp = []
    for n in range((end_date - start_date).days+1):
        tmp.append(start_date + datetime.timedelta(n))
    return tmp



def firmstats(request):
    if request.is_ajax():
        q = request.GET.get('q')
        r = querydate_to_date(request.GET.get('r'))
        s = querydate_to_date(request.GET.get('s'))
        date_range = daterange(r,s)
        avail = 0.0
        sold = 0.0
        purc = 0.0
        pk = int(q)
        for i in date_range:
            dateobj = dateobject.objects.select_related().get(date=i)
            purchase = dateobj.purchase_set.select_related().all()
            for j in purchase:
                if int(j.tab.tag.medicinefirm.pk) == pk:
                    purc += (float(j.nitems))*float(j.tab.actual_price)
                    
            sale = dateobj.invoice_set.select_related().all()
            for j in sale:
                for k in j.tab.all():
                    if int(k.tab.tag.medicinefirm.pk) == pk:
                        sold += float(k.nitems)*float(k.tab.printed_price)
                


        results = [purc, sold]
        return render_to_response( 'firmstats.html', { 'results': results, }) 


