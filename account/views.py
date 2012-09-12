# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.files import File
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
#App import                                                                     
from models import*
import settings
#python import                                                                  
import datetime
import os, sys
import urllib
from search import*
from utils import*
from secview import*

def addinvoice(request):
    item = "["
    price = "["
    vat = "["
    batch = "["
    mname = "["
    patient_ = "["
    phone_ = "["
    patient_name = "["
    year = "["
    month = "["
    credit = "["
    avail ="["
    try:
        invoiceno = str(invoice.objects.order_by('-pk')[0].pk + 1)
    except:
        invoiceno = '1'
    for i in range(10-len(invoiceno)):
        invoiceno = "0" + invoiceno
    tab = list(tablets.objects.select_related().all().order_by('tag__name'))
    for i in tab:
        if i.navailable > 0:
            item += "'" + i.tag.medicinetype.name[:3]+ ". " + i.__unicode__() + "'" 
            price += "'" + i.printed_price + "'" 
            avail += "'" + str(i.navailable) + "'" 
            vat += "'" + str(i.vat) + "'" 
            item += ","
            price += ","
            avail += ","
            vat += ","
            batch += "'" + str(i.batch_no) + "'" 
            batch += ","
            mname += "'" + str(i.tag.name) + "'" 
            mname += ","
            year += str(i.expiry_date.year) 
            year += ","
            month += str(i.expiry_date.month) 
            month += ","
    pat = list(patient.objects.select_related().all().order_by('name'))
    for i in pat:
        patient_ += "'" + str(i.__unicode__().replace('\n','')) + "'" 
        patient_ += ","
        phone_ += "'" + str(i.telephone) + "'" 
        phone_ += ","
        patient_name += "'" + str(i.name.replace('\n','')) + "'" 
        patient_name += ","
        credit += "'" + str(float(i.balance))+ "'"
        credit += ","
    item += "]"
    price += "]"
    vat += "]"
    batch += "]"
    patient_ += "]"
    patient_name += "]"
    phone_ += "]"
    mname += "]"
    month += "]"
    year += "]"
    credit += "]"
    avail += "]"
    return render_to_response('index1.html',{'item':item,'price':price,'vat':vat,'batch':batch,'invoiceno':invoiceno,'patient':patient_,'phone':phone_,'pname':patient_name,'mname':mname,'year':year,'month':month,'credit':credit,'avail':avail})

def readform(request):
    if request.COOKIES.has_key( 'invoiceno' ):
        invoice_no = urllib.unquote(request.COOKIES[ 'invoiceno' ])
    if request.COOKIES.has_key( 'total' ):
        total = urllib.unquote(request.COOKIES[ 'total' ])
    if request.COOKIES.has_key( 'paid' ):
        paid = urllib.unquote(request.COOKIES[ 'paid' ])
    if request.COOKIES.has_key( 'patientname' ):
        patient_name = urllib.unquote(request.COOKIES[ 'patientname' ])
    if request.COOKIES.has_key( 'patient_telephone' ):
        patient_telephone = urllib.unquote(request.COOKIES[ 'patient_telephone' ])
    patient_list = patient.objects.filter(name=patient_name)
    if len(patient_list) != 0:
        for i in patient_list:
            if i.telephone.upper().replace(" ","") == patient_telephone.upper().replace(" ",""):
                patient_ = i
            else:
                tmp_patient = patient(name = patient_name, telephone=patient_telephone, credit_paid='0.0', balance='0.0')
                tmp_patient.save()
                patient_ = tmp_patient
    else:
        tmp_patient = patient(name = patient_name, telephone=patient_telephone, credit_paid='0.0', balance='0.0')
        tmp_patient.save()
        patient_ = tmp_patient
        

    if request.COOKIES.has_key( 'date' ):
        invoice_date = urllib.unquote(request.COOKIES[ 'date' ])
    if request.COOKIES.has_key( 'nmedicine' ):
        n_medicine = urllib.unquote(request.COOKIES[ 'nmedicine' ])
    n_medicine = int(n_medicine)
    medicine_des = []
    for i in range(n_medicine):
        if request.COOKIES.has_key( 'medicine_'+str(i) ):
            medicine_des.append(urllib.unquote(request.COOKIES[ 'medicine_'+str(i) ]))
    is_ok = True
    is_done = False
    if n_medicine == 0:
        is_ok = False
    #data validation need to be done
    #Check for no quantity
    for i in medicine_des:
        medicine_detail = extract_medicine_detail(i)
        try:
            mquantity = int(medicine_detail[2])
        except:
            is_ok = False
    if is_ok == True:
        items_list = []
        for i in medicine_des:
            medicine_detail = extract_medicine_detail(i)
            mname = medicine_detail[0]
            mbatch = medicine_detail[1]
            mquant = medicine_detail[2]
            
            try:
                tmp_tab = tablets.objects.filter(tag__name=mname,batch_no=mbatch)[0]
            except:
                is_ok = False
        
        if is_ok == True:        
            for i in medicine_des:
                medicine_detail = extract_medicine_detail(i)
                mname = medicine_detail[0]
                mbatch = medicine_detail[1]
                mquant = medicine_detail[2]
                try:
                    tmp_tab = tablets.objects.filter(tag__name=mname,batch_no=mbatch)[0]
                    tmp_tab._sale(int(mquant))
                    tmp_item = invoiceitem(tab=tmp_tab, nitems=int(mquant))
                    tmp_item.save()
                    items_list.append(tmp_item)
                    med = tmp_item.tab.tag
                    med.consumption_rate *= int(invoice_no)-1 
                    med.consumption_rate += (tmp_item.nitems)
                    med.consumption_rate /= float(int(invoice_no))
                    med.save()
            
                except:
                    is_ok = False
                
        
         
        
    
    invoice_no = str(invoice_no)
    for i in range(10-len(invoice_no)):
        invoice_no = "0" + invoice_no
    for i in invoice.objects.all():
        if invoice_no == i.invoice_no:
            is_ok = False

    try:
        invoiceno = str(invoice.objects.order_by('-pk')[0].pk + 1)
    except:
        invoiceno = '1'
    for i in range(10-len(invoiceno)):
        invoiceno = "0" + invoiceno
        
    medicine_str = ""
    for i in medicine_des:
        medicine_str += i + "&&&"
    tmpdate = invoicedate_to_date(invoice_date)
    if is_ok:
        try:
            dateob = dateobject.objects.get(date=tmpdate)
        except:
            dateob = dateobject(date=tmpdate)
            dateob.save()
        
        tmp_invoice = invoice(invoice_no=invoice_no, patient=patient_, invoice_date=invoice_date, nmedicine=n_medicine, medicine_str=medicine_str, total=total, paid=paid,date=dateob)
        tmp_invoice.date_created = datetime.datetime.now()
        tmp_invoice.date_last_modified = datetime.datetime.now()
        tmp_invoice.save()
        tmp_invoice.tab = items_list
        del items_list
        tmp_invoice.save()
        patient_.balance = (float(patient_.balance) + float(total)-float(paid))
        patient_.save()
        try:
            invoiceno = str(invoice.objects.order_by('-pk')[0].pk + 1)
        except:
            invoiceno = '1'
        for i in range(10-len(invoiceno)):
            invoiceno = "0" + invoiceno
        return render_to_response('invoiceform.html',{'invoiceno':invoiceno})    
    else:
        return render_to_response('invoiceform.html',{'invoiceno':invoiceno,'error':'Last Invoice Not Submitted'})    
    return HttpResponseRedirect('/')

def addstock(request):
    item = "["
    for i in medicine.objects.order_by('name'):
        item += "'" + i.name + "'" 
        item += ","
    item += "]"
    pharma_shop = "["
    for i in pharmashop.objects.all():
        pharma_shop += "'" + str(i.name) + "'" 
        pharma_shop += ","
    pharma_shop += "]"
    try:
        q = request.GET.get('q')
        tmp_tablets = tablets.objects.get(pk=int(q))
        return render_to_response('stockadd.html',{'item':item,'pharmashop':pharma_shop,'tab':tmp_tablets})
    except:
        return render_to_response('stockadd.html',{'item':item,'pharmashop':pharma_shop})

def addstockprocess(request):
    if request.method == "POST":
        form = stockform(request.POST)
        tag_name = form.data.get('tag_name')
        batch_no = form.data.get('batch_no')
        expiry_date = form.data.get('expiry_date')
        actual_price = form.data.get('actual_price')
        printed_price = form.data.get('printed_price')
        vat = form.data.get('vat')
        pharma_shop = form.data.get('pharma_shop')
        nmedicine = form.data.get('nmedicine')
        actual_price = str(round(eval(actual_price),2))
        printed_price = str(round(eval(printed_price),2))
        for j in medicine.objects.all():
            if j.name.upper().replace(" ","") == \
                    tag_name.upper().replace(" ",""):
                tag = j
            
        
        tab_list = tablets.objects.filter(tag=tag)
        is_found = False
        if len(tab_list) != 0:
            for i in tab_list:
                if i.batch_no.upper().replace(" ","") == \
                        batch_no.upper().replace(" ",""):
                    i.navailable += int(nmedicine)          
                    i.revision_history += nmedicine + "___" + datetime.datetime.now().ctime() +"___" + pharma_shop + "&&&"
                    i.save()
                    is_found = True
                    print pharma_shop
                    pharma__shop = pharmashop.objects.filter(name=pharma_shop)[0]
                    try:
                        dateob = dateobject.objects.get(date=datetime.date.today())
                    except:
                        dateob = dateobject(date=datetime.date.today())
                        dateob.save()
                        
                    tmpp = purchase(tab=i,nitems=int(nmedicine),date=dateob, pharmashop=pharma__shop)
                    tmpp.save()

               
        if len(tab_list) == 0 or is_found == False:
            for j in pharmashop.objects.all():
                if j.name.upper().replace(" ","") == \
                        pharma_shop.upper().replace(" ",""):
                    pharma__shop = j
                
            try:
                dateob = dateobject.objects.get(date=datetime.date.today())
            except:
                dateob = dateobject(date=datetime.date.today())
                dateob.save()


            

            tmp_tablet = tablets(tag=tag, expiry_date=expiry_date, purchased_date=datetime.datetime.now(), batch_no=batch_no, actual_price=actual_price, printed_price=printed_price,navailable=int(nmedicine), vat=vat, pharma_shop=pharma__shop)
            tmp_tablet.revision_history += nmedicine + "___" + datetime.datetime.now().ctime() +"___" + pharma_shop + "&&&"
            tmp_tablet.save()
            tmpp = purchase(tab=tmp_tablet,nitems=int(nmedicine),date=dateob,\
                                pharmashop=pharma__shop)
            tmpp.save()

        return HttpResponseRedirect('/stock_add')
    else:
        return HttpResponseRedirect('/')

def addmedicine(request):
    try:
        print request.REQUEST['info']
    except:
        pass
    item = "["
    for i in medicine.objects.all():
        item += "'" + i.name + "'" 
        item += ","
    
        
    item += "]"
    
    firm = "["
    for i in medicinefirm.objects.all():
        firm += "'" + str(i.name) + "'" 
        firm += ","
    firm += "]"
    mtype = "["
    for i in medicinetype.objects.all():
        mtype += "'" + str(i.name) + "'" 
        mtype += ","
    mtype += "]"
    
   
    
    return render_to_response('medicineadd.html',{'tag_name':item,'mtype':mtype,'firm':firm})


def addmedicineprocess(request):
    if request.method == "POST":
        form = medicineform(request.POST)
        tag_name = form.data.get('tag_name')
        firm_name = form.data.get('firm')
        medicine_type = form.data.get('mtype')
        is_found = False
        for i in medicine.objects.all():
            if i.name.upper().replace(" ","") ==\
                    tag_name.upper().replace(" ",""):
                is_found = True
                return HttpResponseRedirect("/medicine_add")
        
        if is_found == False:
            if_firm = False
            if_type = False
            for j in medicinefirm.objects.all():
                if j.name.upper().replace(" ","") ==\
                        firm_name.upper().replace(" ",""):
                    firm_obj = j
                    if_firm = True
            if if_firm == False:
                tmp_medicinefirm = medicinefirm(name=firm_name)
                tmp_medicinefirm.save()
                firm_obj = tmp_medicinefirm
            
            for j in medicinetype.objects.all():
                if j.name.upper().replace(" ","") ==\
                        medicine_type.upper().replace(" ",""):
                    type_obj = j
                    if_type = True
            if if_type == False:
                tmp_medicinetype = medicinetype(name=medicine_type)
                tmp_medicinetype.save()
                type_obj = tmp_medicinetype
            tmp_medicine = medicine(name=tag_name, medicinefirm=firm_obj, medicinetype=type_obj)
            tmp_medicine.save()
            response = HttpResponseRedirect("/medicine_add")
            response['info'] = 'info'
            return response
        
    else:
        return HttpResponseRedirect("/")

def addfirm(request):
    firm = "["
    for i in medicinefirm.objects.all():
        firm += "'" + str(i.name) + "'" 
        firm += ","
    firm += "]"
    return render_to_response('firmadd.html',{'firm':firm})

def addfirmprocess(request):
    if request.method == "POST":
        form = medicinefirmform(request.POST)
        tag_name = form.data.get('tag_name')
        is_found = False
        for i in medicinefirm.objects.all():
            if i.name.upper().replace(" ","") ==\
                    tag_name.upper().replace(" ",""):
                is_found = True
                return HttpResponseRedirect("/firm_add")
        if is_found == False:
            tmp_medicinefirm = medicinefirm(name=tag_name)
            tmp_medicinefirm.save()
            return HttpResponseRedirect("/firm_add")
    else:
        return HttpResponseRedirect("/")
def addtype(request):
    mtype = "["
    for i in medicinetype.objects.all():
        mtype += "'" + str(i.name) + "'" 
        mtype += ","
    mtype += "]"
    return render_to_response('typeadd.html',{'type':mtype})

def addtypeprocess(request):
    if request.method == "POST":
        form = medicinetypeform(request.POST)
        tag_name = form.data.get('tag_name')
        is_found = False
        for i in medicinetype.objects.all():
            if i.name.upper().replace(" ","") ==\
                    tag_name.upper().replace(" ",""):
                is_found = True
                return HttpResponseRedirect("/type_add")
        if is_found == False:
            tmp_medicinetype = medicinetype(name=tag_name)
            tmp_medicinetype.save()
            return HttpResponseRedirect("/type_add")
    else:
        return HttpResponseRedirect("/")
def addpharma(request):
    pharma = "["
    for i in pharmashop.objects.all():
        pharma += "'" + str(i.name) + "'" 
        pharma += ","
    pharma += "]"
    return render_to_response('pharmaadd.html',{'pharma':pharma})

def addpharmaprocess(request):
    if request.method == "POST":
        form = pharmaform(request.POST)
        tag_name = form.data.get('tag_name')
        phone = form.data.get('phone')
        is_found = False
        for i in pharmashop.objects.all():
            if i.name.upper().replace(" ","") ==\
                    tag_name.upper().replace(" ",""):
                is_found = True
                return HttpResponseRedirect("/pharma_add",{'info':""})
        if is_found == False:
            tmp_pharmashop = pharmashop(name=tag_name,telephone=phone)
            tmp_pharmashop.save()
            return HttpResponseRedirect("/pharma_add")
    else:
        return HttpResponseRedirect("/")

def profit_calculator():
    sale = 0.0
    purchase = 0.0
    stock = 0.0
    credit = 0.0
    for i in tablets.objects.all():
        sale += float(i.printed_price)*int(i.nsold)
        purchase += float(i.actual_price)*int(i.nsold+i.navailable)
        stock += float(i.actual_price)*int(i.navailable)
    for i in invoice.objects.all():
        credit += float(i.total) - float(i.paid)
    for i in patient.objects.all():
        for j in i.creditobject_set.all():
            credit -= float(j.amount)
    return [sale, purchase, stock, credit]
def dash(request):
    sale, purchase, stock, credit = profit_calculator()
    try:
        maxinvoiceno = invoice.objects.order_by('-pk')[0].pk
    except:
        maxinvoiceno = 1
    return render_to_response('dashboard.html',{'sale':sale,'purchase':purchase,'stock':stock,'credit':credit,'maxinvoiceno':maxinvoiceno})

def generate_stock_row(i):
    stock_str = ''
    stock_str += '<tr>'
    stock_str += '<td>' + i.tag.name + '</td>'
    stock_str += '<td>' + i.batch_no + '</td>'
    stock_str += '<td>' + str(i.expiry_date.month)+'/'+str(i.expiry_date.year) + '</td>'
    stock_str += '<td>' + str(i.actual_price) + '</td>'
    stock_str += '<td>' + i.printed_price + '</td>'
    stock_str += '<td>' + str(i.navailable) + '</td>'
    stock_str += '<td>' + str(i.nsold) + '</td>'
    stock_str += '<td><a href=/stock_edit/'+str(i.pk)+' target=_blank/>Edit</a> / <a href=/stock_add/?q='+str(i.pk)+' target=_blank/>Add</a></td>'
    #stock_str += "<td><button onclick='myFunction("+str(i.pk)+")'"+str(i.pk)+'/>Delete</button></td>'
    stock_str += '</tr>'
    return stock_str
def generate_patient_row(i):
    stock_str = ''
    stock_str += '<tr>'
    stock_str += '<td>' + i.name + '</td>'
    stock_str += '<td>' + i.telephone + '</td>'
    
    tmp_invoice = i.invoice_set.all()
    credit = float(i.balance)
   
    
    stock_str += '<td>Rs. ' + str(credit) + '</td>'
    stock_str += '<td><a href=/credit_view_details/'+str(i.pk)+'/>view</a></td>'
    stock_str += '</tr>'
    return [stock_str, credit]


def viewstock(request):
    stock_str = ''
    tab = list(tablets.objects.select_related().order_by('tag__name'))
    for i in tab:
        if i.navailable > 0:
            stock_str += generate_stock_row(i)
    return render_to_response('stockview.html',{'stock_str':stock_str})

def editstock(request, pid):
    item = "["
    for i in medicine.objects.order_by('name'):
        item += "'" + i.name + "'" 
        item += ","
    item += "]"
    pharma_shop = "["
    for i in pharmashop.objects.all():
        pharma_shop += "'" + str(i.name) + "'" 
        pharma_shop += ","
    pharma_shop += "]"

    tmp_stock = tablets.objects.get(pk=pid)
    tmp_date = str(tmp_stock.expiry_date.year) + "-" 
    tmp1 = str(tmp_stock.expiry_date.month) 
    tmp2 = str(tmp_stock.expiry_date.day) 
    if len(tmp1) == 1:
        tmp1 = "0" + tmp1
    if len(tmp2) == 1:
        tmp2 = "0" + tmp2
    tmp_date += tmp1 + "-" + tmp2 

    return render_to_response('stockedit.html',{'tmp_stock':tmp_stock,'tmp_date':tmp_date,'item':item,'pharmashop':pharma_shop})


def editstockprocess(request):
    if request.method == "POST":
        form = stockform(request.POST)
        tag_name = form.data.get('tag_name')
        batch_no = form.data.get('batch_no')
        expiry_date = form.data.get('expiry_date')
        actual_price = form.data.get('actual_price')
        printed_price = form.data.get('printed_price')
        vat = form.data.get('vat')
        pharma_shop = form.data.get('pharma_shop')
        nmedicine = form.data.get('nmedicine')
        tab_list = tablets.objects.filter(batch_no=batch_no)
        if len(tab_list) != 0:
            for i in tab_list:
                if i.tag.name.upper().replace(" ","") == \
                        tag_name.upper().replace(" ",""):
                    tmp_n = int(nmedicine) - int(i.navailable)
                    i.revision_history += str(tmp_n) + "___" + datetime.datetime.now().ctime() + "___" + pharma_shop +  "&&&"
                    i.navailable = int(nmedicine)
                    i.save()
                    pharma__shop = pharmashop.objects.filter(name=pharma_shop)[0]
                    try:
                        dateob = dateobject.objects.get(date=datetime.date.today())
                    except:
                        dateob = dateobject(date=datetime.date.today())
                        dateob.save()
                        
                    tmpp = purchase(tab=i,nitems=int(tmp_n),date=dateob, pharmashop=pharma__shop)
                    tmpp.save()

                    tmptmp = i
               
        return HttpResponseRedirect('/stock_edit/'+str(tmptmp.pk)+'/')
    else:
        return HttpResponseRedirect('/')

def deletestock(request, pid):
    tmp_stock = tablets.objects.get(pk=pid)
    tmp_stock.delete()
    return HttpResponseRedirect('/stock_view/')

def searchlist(request):
    if request.method == 'POST':
        form = search_form(request.POST)
        if form.is_valid():
            query = form.data.get('query')
            t = tablets.objects.select_related().order_by('tag')
            b = get_results(t, query, ['tag.name','batch_no','tag.medicinefirm.name'])
            stock_str = 'Displaying search results for <b>'+query+'</b> <br>Go back to <a href=/stock_view/>stock view</a><br>'
            if len(b) != 0:
                for i in b:
                    stock_str += generate_stock_row(i)
            else:
                stock_str += "No results found"
            
            return render_to_response('stockview.html',{'stock_str':stock_str})
        else:
            return HttpResponseRedirect('/stock_view/')

def searchlist_patient(request):
    if request.method == 'POST':
        form = search_form(request.POST)
        if form.is_valid():
            query = form.data.get('query')
            t = patient.objects.select_related().order_by('name')
            b = get_results(t, query, ['name','telephone'])
            stock_str = 'Displaying search results for <b>'+query+'</b> <br>Go back to <a href=/credit_view/>credit view</a><br>'
            if len(b) != 0:
                for i in b:
                    stock_str += generate_patient_row(i)[0]
            else:
                stock_str += "No results found"
            
            return render_to_response('creditview.html',{'patient_str':stock_str})
        else:
            return HttpResponseRedirect('/credit_view/')
            


def viewcredit(request):
    stock_str = ''
    for i in patient.objects.select_related().all():
        tmp = generate_patient_row(i)
        if tmp[1] > 5.0:
            stock_str += tmp[0]
    return render_to_response('creditview.html',{'patient_str':stock_str})

def generate_invoice_row(i):
    stock_str = ''
    stock_str += '<tr>'
    stock_str += '<td>' + i.invoice_no + '</td>'
    stock_str += '<td>' + i.invoice_date + '</td>'
    stock_str += '<td>' + i.total + '</td>'
    stock_str += '<td>' + i.paid + '</td>'
    stock_str += '<td>' + str(float(i.total)-float(i.paid)) + '</td>'
    stock_str += '<td><a href=/invoice_view/'+str(i.pk)+'/ target=_blank>view</a>/<a href=/invoice_print/'+str(i.pk)+'/ target=_blank>print</a></td>'
    stock_str += '</tr>'
    return stock_str


def viewcreditdetails(request, pid):
    tmp_patient = patient.objects.get(pk=pid)
    tmp_history = ""
    hlist = tmp_patient.credit_history.split('&&&')[:-1]
    hlist.reverse()
    for i in hlist:
        amount = i.split('___')[0]
        stime = i.split('___')[1]
        tmp_history += "<li>"
        tmp_history += "Rs. " + amount + " paid on "
        tmp_history +=  stime + "<br>"
        tmp_history += "</li>"
    
    tmp_invoices = tmp_patient.invoice_set.all()
    stock_str = ''
    for i in tmp_invoices:
        stock_str += generate_invoice_row(i)
    
    stock_str += '<hr><tr><td>Credit Paid</td><td>'
    stock_str += tmp_patient.credit_paid
    stock_str += '</td><td></td><td>To be Paid</td><td>'
    credit = float(tmp_patient.balance)
    stock_str += str(credit) + '</td><td></td></tr>'
    
    return render_to_response('creditviewdetails.html',{'invoice_str':stock_str, 'patient':tmp_patient,'credit_history':tmp_history})

def viewinvoice(request, pid):
    tmp_invoice = invoice.objects.get(pk=pid)
    tablets_list = extract_tablets_list(tmp_invoice.medicine_str)
    tmp_str = ''

    for j in tablets_list[:-1]:
        medicine_detail = extract_medicine_detail(j)
        tmp_name = medicine_detail[0]
        tmp_batch = medicine_detail[1]
        tmp_quantity = medicine_detail[2]
        tmp_medicine = tablets.objects.filter(batch_no=tmp_batch.replace(" ",''))
        for k in tmp_medicine:
            print k
            if k.tag.name.upper().replace(" ","") == tmp_name.upper().replace(" ",""):
                tmp_mrp = k.printed_price
                tmp_vat = k.vat
        tmp_str += generate_invoice_medicine_row(tmp_name, tmp_batch, tmp_mrp, tmp_quantity, str(int(tmp_quantity)*float(tmp_mrp)), tmp_vat, str(int(tmp_quantity)*float(tmp_mrp)*(1+float(tmp_vat)/100.0)))
    balance = str(float(tmp_invoice.total) - float(tmp_invoice.paid))
    return render_to_response('invoiceview.html',{'invoice':tmp_invoice, 'tmp_str':tmp_str,'balance':balance})

def generate_invoice_medicine_row(itemname, batch_no, unitcost, quantity, price, vat, amount):
     tmp_str = "<tr class='item-row'><td><span class='item-name' id='autocomplete'  readonly='readonly'>"
     tmp_str += itemname
     tmp_str += "</span></td><td><span class='batch'  readonly='readonly'>"
     tmp_str += batch_no
     tmp_str += "</span></td><td><span class='cost'  readonly='readonly'>"
     tmp_str += unitcost
     tmp_str += "</span></td><td><span class='quantity'  readonly='readonly'>"
     tmp_str += quantity
     tmp_str += "</span></td><td><span class='price'>"
     tmp_str += price
     tmp_str += "</span></td><td><span class='vat'  readonly='readonly'>"
     tmp_str += vat
     tmp_str += "</span></td><td><span class='amount'>"
     tmp_str += amount 
     tmp_str += "</span></td></tr>"
     return tmp_str

def addcreditamount(request):
    if request.method == 'POST':
        form = credit_form(request.POST)
        if form.is_valid():
            ntime = datetime.datetime.now()
            stime = ntime.ctime()
            amount = form.data.get('amount')
            pid = form.data.get('pid')
            tmp_patient = patient.objects.get(pk=int(pid))
            if tmp_patient.credit_paid == '':
                tmp_patient.credit_paid = str(float(amount))
            else:
                tmp_patient.credit_paid = str(float(tmp_patient.credit_paid) + float(amount))
            tmp_patient.credit_history += amount + "___" + stime + "&&&"
            tmp_patient.balance = str(float(tmp_patient.balance) - float(amount))
            tmp_patient.save()
            try:
                dateobj = dateobject.objects.get(date=datetime.date.today())
            except:
                dateobj = dateobject(date=datetime.date.today())
                dateobj.save()
            tmp = creditobject(amount=amount,patient=tmp_patient,date=dateobj)
            tmp.save()
            return HttpResponseRedirect('/credit_view_details/'+pid+'/')

def generate_small_stock_row(i):
    stock_str = ''
    stock_str += '<tr>'
    stock_str += '<td>' + i.tag.name + '</td>'
    stock_str += '<td>' + i.batch_no + '</td>'
    stock_str += '<td>' + str(i.expiry_date.month)+'/'+str(i.expiry_date.year) + '</td>'
    stock_str += '<td>' + i.printed_price + '</td>'
    stock_str += '<td>' + str(i.navailable) + '</td>'
    stock_str += '<td>' + str(i.nsold) + '</td>'
    stock_str += '<td><button onclick=myFunction('+str(i.pk)+",'"+i.tag.name.replace(' ','')+"')>remove</button></td>"

    stock_str += '</tr>'
    return stock_str


def viewexpiry(request):
    if request.method == 'POST':
        form = expiry_form(request.POST)
        if form.is_valid():
            query = form.data.get('query')
            nday = int(query)
            tmp_str = ''
            ftime = datetime.datetime.now() + datetime.timedelta(days=nday)
            info = "Medicines expiring before <b>" + ftime.date().ctime().replace("00:00:00 ","") + "</b>"
            is_date = False
            tab = list(tablets.objects.select_related().order_by('expiry_date'))
            for i in tab:
                if i.expiry_date.date() < ftime.date():
                    if i.navailable > 0:
                        is_date = True
                        tmp_str += generate_small_stock_row(i)
                else:
                    if is_date == True:
                        break
            return render_to_response('expiryview.html',{'stock_str':tmp_str, 'info':info})
    else:
        return render_to_response('expiryview.html')

def generate_einvoice_medicine_row(itemname, batch_no, unitcost, quantity, price, vat, amount):
     tmp_str = "<tr class='item-row'><td><textarea class='item-name' id='autocomplete'  readonly='readonly'>"
     tmp_str += itemname
     tmp_str += "</textarea></td><td><textarea class='batch'  readonly='readonly'>"
     tmp_str += batch_no
     tmp_str += "</textarea></td><td><textarea class='cost'  readonly='readonly'>"
     tmp_str += unitcost
     tmp_str += "</textarea></td><td><textarea class='quantity'>"
     tmp_str += quantity
     tmp_str += "</textarea></td><td><span class='price'>"
     tmp_str += price
     tmp_str += "</span></td><td><textarea class='vat'  readonly='readonly'>"
     tmp_str += vat
     tmp_str += "</textarea></td><td><span class='amount'>"
     tmp_str += amount 
     tmp_str += "</span></td></tr>"
     return tmp_str


def editinvoice(request, pid):
    tmp_invoice = invoice.objects.get(pk=pid)
    tablets_list = extract_tablets_list(tmp_invoice.medicine_str)
    tmp_str = ''
   
    for j in tablets_list[:-1]:
        medicine_detail = extract_medicine_detail(j)
        tmp_name = medicine_detail[0]
        tmp_batch = medicine_detail[1]
        tmp_quantity = medicine_detail[2]
        tmp_medicine = tablets.objects.filter(batch_no=tmp_batch.replace(" ",''))
        for k in tmp_medicine:
            if k.tag.name.upper().replace(" ","") == tmp_name.upper().replace(" ",""):
                tmp_mrp = k.printed_price
                tmp_vat = k.vat
        tmp_str += generate_einvoice_medicine_row(tmp_name, tmp_batch, tmp_mrp, tmp_quantity, str(int(tmp_quantity)*float(tmp_mrp)), tmp_vat, str(int(tmp_quantity)*float(tmp_mrp)*(1+float(tmp_vat)/100.0)))
    balance = str(float(tmp_invoice.total) - float(tmp_invoice.paid))
    return render_to_response('invoiceedit.html',{'invoice':tmp_invoice, 'tmp_str':tmp_str,'balance':balance})

def ereadform(request):
    if request.COOKIES.has_key( 'invoiceno' ):
        invoice_no = urllib.unquote(request.COOKIES[ 'invoiceno' ])
    if request.COOKIES.has_key( 'total' ):
        total = urllib.unquote(request.COOKIES[ 'total' ])
    if request.COOKIES.has_key( 'paid' ):
        paid = urllib.unquote(request.COOKIES[ 'paid' ])
    if request.COOKIES.has_key( 'patientname' ):
        patient_name = urllib.unquote(request.COOKIES[ 'patientname' ])
    if request.COOKIES.has_key( 'patient_telephone' ):
        patient_telephone = urllib.unquote(request.COOKIES[ 'patient_telephone' ])
    patient_list = patient.objects.filter(telephone=patient_telephone)
    if len(patient_list) != 0:
        for i in patient_list:
            if i.name.upper().replace(" ","") == patient_name.upper().replace(" ",""):
                patient_ = i
        

    if request.COOKIES.has_key( 'date' ):
        invoice_date = urllib.unquote(request.COOKIES[ 'date' ])
    if request.COOKIES.has_key( 'nmedicine' ):
        n_medicine = urllib.unquote(request.COOKIES[ 'nmedicine' ])
    n_medicine = int(n_medicine)
    medicine_des = []
    for i in range(n_medicine):
        if request.COOKIES.has_key( 'medicine_'+str(i) ):
            medicine_des.append(urllib.unquote(request.COOKIES[ 'medicine_'+str(i) ]))
    is_ok = True
    if n_medicine == 0:
        is_ok = False
    invoice_no = str(invoice_no)
    for i in range(10-len(invoice_no)):
        invoice_no = "0" + invoice_no
        
    tmp_invoice = invoice.objects.filter(invoice_no=invoice_no)[0]
    med_list = tmp_invoice.medicine_str.split('&&&')
    
    items_list = []    
    for k in range(len(medicine_des)):
        oname = med_list[k].split('___')[0]
        obatch = med_list[k].split('___')[1]
        oquantity = int(med_list[k].split('___')[2])

        medicine_detail = extract_medicine_detail(medicine_des[k])
        mname = medicine_detail[0]
        mbatch = medicine_detail[1]
        mquantity = int(medicine_detail[2])

        for j in medicine.objects.all():
            if j.name.upper().replace(" ","") == \
                    mname.upper().replace(" ",""):
                tag = j
            
        
        tab_list = tablets.objects.filter(tag=tag)
       
        for i in tab_list:
            print i.batch_no.upper().replace(" ",""),mbatch
            if i.batch_no.upper().replace(" ","") == mbatch.upper().replace(" ",""):
                
                nrem = i.navailable - (mquantity - oquantity)
                if  nrem >= 0:
                    i.navailable -= (mquantity-oquantity) 
                    i.nsold += (mquantity-oquantity)
                    mquant = (mquantity-oquantity)
                    i.save()
                    tmp_item = invoiceitem(tab=i, nitems=int(mquant))
                    tmp_item.save()
                    items_list.append(tmp_item)
                    
                else:
                    print "Stock Unavailable"
            else:
                is_ok = False
    medicine_str = ""
    for i in medicine_des:
        medicine_str += i + "&&&" 
    if is_ok:
        
        tmp_invoice.total = total
        tmp_invoice.paid = paid
        tmp_invoice.medicine_str = medicine_str
        tmp_invoice.date_last_modified = datetime.datetime.now()
        tmp_invoice.tab = items_list
        tmp_invoice.save()
        return HttpResponseRedirect('/')
    else:
        raise Http404
    return HttpResponseRedirect('/')


def generate_demand_row(name, quan, pk):
    stock_str = ''
    stock_str += '<tr>'
    stock_str += '<td id=check>' +"<input type=checkbox name='done' id='done' value="+str(pk)+ " style='width:10px' >" + '</td>'
    stock_str += '<td>' + name + '</td>'
    stock_str += '<td>' + str(quan) + '</td>'
    stock_str += '</tr>'
    return stock_str



def viewdemand(request):
    stock_str = ''
    med = list(medicine.objects.select_related().order_by('medicinetype__name'))
    for i in med:
        tmp_tab = list(i.tablets_set.select_related().all())        
        count = 0
        for j in tmp_tab:
            count += j.navailable
        if count < i.medicinetype.minno:
            if len(tmp_tab) != 0:
                stock_str += generate_demand_row(i.medicinetype.name[:3] +". " + i.name, count, i.pk)
    return render_to_response('demandview.html',{'stock_str':stock_str})
    
   

def printinvoice(request):
    pass

def remove_expired(request, pid):
    i = tablets.objects.get(pk=int(pid))
    pharma_shop = i.pharma_shop
    tmp_n = - int(i.navailable)
    i.revision_history += str(tmp_n) + "___" + datetime.datetime.now().ctime() + "___" + pharma_shop.name +  "&&&"
    i.navailable = 0.0
    i.save()
    
    try:
        dateob = dateobject.objects.get(date=datetime.date.today())
    except:
        dateob = dateobject(date=datetime.date.today())
        dateob.save()
                        
    tmpp = purchase(tab=i,nitems=int(tmp_n),date=dateob, pharmashop=pharma_shop)
    tmpp.save()

    tmptmp = i
               
    return HttpResponseRedirect('/stock_edit/'+str(tmptmp.pk)+'/')
