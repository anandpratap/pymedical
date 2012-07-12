from account.models import*
from account.secview import*
_invoice = invoice.objects.all()
for i in _invoice:
    tmpdate = invoicedate_to_date(i.invoice_date)
    try:
        dateob = dateobject.objects.get(date=tmpdate)
    except:
        dateob = dateobject(date=tmpdate)
        dateob.save()
    i.date = dateob
    i.save()
#above code can be run multiple times but be careful with the below one
for i in tablets.objects.all():
    print i
    rev = i.revision_history.split('&&&')[:-1]
    for j in rev:
        tmp = j.split('___')
        try:
            pharma = tmp[2]
        except:
            pass
        nitems = int(tmp[0])
        _pharmashop = pharmashop.objects.filter(name=pharma)[0]
        tmpdate = ctime_to_date(tmp[1])
        try:
            dateob = dateobject.objects.get(date=tmpdate)
        except:
            dateob = dateobject(date=tmpdate)
            dateob.save()
   
            
        tmpp = purchase(tab=i,nitems=nitems,date=dateob,pharmashop=_pharmashop)
        tmpp.save()
