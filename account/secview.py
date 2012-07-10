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

def process_latex(title_1, title_2, table, info):
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)        
    texfile, texfilename = mkstemp(dir=tmp_folder)
    os.write(texfile, render_to_string('sam1.tex', {'table': table, 'title_1':title_1, 'title_2':title_2, 'info':info}))
    os.close(texfile)
    for i in range(2):
        call(['pdflatex', texfilename])
    texfilename = texfilename + ".pdf"
    return texfilename


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
    

def latex_invoice_list(i):
    return i.invoice_no + "&" +  i.patient.name + "&" + str(i.nmedicine) + "& Rs. " + str(i.total) + "& Rs. " + str(i.paid) + "\\\\" 


def latex_daily_str(request):
    q = querydate_to_date(request.GET.get('q'))
    #_str = '\\begin{supertabular}{|lp{3 cm}cll|}\\hline '
    _str = '\centering\\textbf{Sale}'
    _str += """\\begin{longtable}{l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l}\\hline"""
    _str += ' Invoice No. & Patient Name & No. Item & Total & Paid\\\\\hline'
    
    for i in invoice.objects.all():
        _date = invoicedate_to_date(i.invoice_date)
        if matchdate(_date, q):
            _str += latex_invoice_list(i)
    _daily = dailycps(q)
    _str += "\\hline"
    _str += '& & Total: & Rs. '+str(_daily[2]) + "& Rs. " + str(_daily[2]-_daily[0]) + "\\\\" 
    _str += '\\hline\end{longtable}'
    _str += '\centering\\textbf{Purchase}'
    _str += """\\begin{longtable}{l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l}\\hline"""
    _str += ' Pharma Shop & Item Name & Batch No. & Rate  & N Item & Amount\\\\\hline '
    
    for i in tablets.objects.order_by('tag__name'):
        t = i.revision_history.split('&&&')
        for j in t[:-1]:
            deta = j.split('___')
            try:
                mname = deta[2]
            except:
                pass
            mquan = deta[0]
            mday = deta[1]
            _date = ctime_to_date(mday)
            if matchdate(q, _date):
                _str += mname + " & " + i.tag.name + " & "  + i.batch_no + " & " + i.actual_price + " & "  + mquan + " & " + str(int(mquan)*float(i.actual_price)) + " \\\\"
    _str += '\\hline\end{longtable}'
    title_1 = "Daily Balance Sheet"
    title_2 = "Dated: " + q.ctime().replace("00:00:00 ",'')
    info = "Total Sale: Rs. " + str(_daily[2]) + "\\\\" + "Total Purchase: Rs. " + str(_daily[1]) + "\\\\Total Credit: Rs. " + str(_daily[0])+"\\\\"
    texfilename = process_latex(title_1, title_2, _str, info)
    response = HttpResponse(file(texfilename).read())
    response['Content-Type'] = 'application/pdf'
    filename = 'Balancesheet_'+ q.ctime().replace("00:00:00 ",'')
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response


def daterange(start_date, end_date):
    tmp = []
    for n in range((end_date - start_date).days+1):
        tmp.append(start_date + datetime.timedelta(n))
    return tmp


def latex_print_str(request):
    p = querydate_to_date(request.GET.get('p'))
    q = querydate_to_date(request.GET.get('q'))
    _dates = daterange(p,q)
    results = [0, 0, 0]
    _str = """\\begin{longtable}{l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l}\\hline"""
    _str += ' Date & Total Sale (Rs.) & Total Purchase (Rs.) & Credit (Rs.)\\\\\hline'

    for i in _dates:
        for j in range(3):
            results[j] += dailycps(i)[j]
        _str += properdate(i) + "&" +  \
            str(dailycps(i)[2]) + "&" + str(dailycps(i)[1]) + "&" + str(dailycps(i)[0]) + "\\\\\penlt"
    _str += '\\hline'
    _str += ' Total: & Rs. '+str(results[2]) + "& Rs. " + str(results[1]) + "& Rs. " + str(results[0]) +"\\\\" 
    _str += '\\hline\end{longtable}'
    title_1 = "Balance Sheet"
    title_2 = "From: " + p.ctime().replace("00:00:00 ",'') + " To: "+ q.ctime().replace("00:00:00 ",'')
    info = "Total Sale: Rs. " + str(results[2]) + "\\\\" + "Total Purchase: Rs. " + str(results[1]) + "\\\\Total Credit: Rs. " + str(results[0])+"\\\\"
    texfilename = process_latex(title_1, title_2, _str, info)
    response = HttpResponse(file(texfilename).read())
    response['Content-Type'] = 'application/pdf'
    filename = 'Balance Sheet'+ p.ctime().replace("00:00:00 ",'') + " to "+ q.ctime().replace("00:00:00 ",'')
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response
 

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

def latex_stock_str(count, i):
    return str(count) + " & "+ i.tag.name + "&" +  i.batch_no + "&" + str(i.expiry_date.month) + "/" +str(i.expiry_date.year) + " & Rs. " + str(i.actual_price) + "& Rs. " + str(i.printed_price) +" & " + str(i.navailable) + " & " +str(i.nsold) + "\\\\ " 
    
def latex_total_stock_str(request):
    _str = """\\begin{longtable}{l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l}\\hline"""
    _str += ' No. & Name & Batch No. & Expiry & Rate & MRP & Available & Sold\\\\\hline '
    count = 0
    for i in tablets.objects.order_by('tag__name'):
        count += 1
        _str += latex_stock_str(count, i)
       
    _str += '\\hline\end{longtable}'
    
    title_1 = "Total Stock Sheet"
    title_2 = "Dated: " + datetime.datetime.now().ctime()
    info = ''
    texfilename = process_latex(title_1, title_2, _str, info)
    response = HttpResponse(file(texfilename).read())
    response['Content-Type'] = 'application/pdf'
    filename = 'Total Stock '+ datetime.datetime.today().ctime().replace("00:00:00 ",'')
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response


def pdfdemand(request):
    if request.COOKIES.has_key( 'demand' ):
        demand = urllib.unquote(request.COOKIES[ 'demand' ])
    demand = demand.split('___')

    _str = """\\begin{longtable}{l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}l@{\extracolsep{\\fill}}|l}\\hline"""
    _str += ' No. &  Name & Company & Pharma & Quantity\\\\\hline '
    
    counter = 0
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
                _str +=  str(counter) + " & "+ i.medicinetype.name[:3] + ". " + i.name + " & " + i.medicinefirm.name + " & " + pharma_name + "&\\\\\hline " 
                

    _str += '\\hline\end{longtable}'
    
    title_1 = "Demand Stock Sheet"
    title_2 = "Dated: " + datetime.datetime.now().ctime()
    info = ''
    texfilename = process_latex(title_1, title_2, _str, info)
    response = HttpResponse(file(texfilename).read())
    response['Content-Type'] = 'application/pdf'
    filename = 'Total Demand '+ datetime.datetime.today().ctime().replace("00:00:00 ",'')
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response


