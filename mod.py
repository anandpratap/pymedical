from account.models import*

tmp = invoice.objects.all()

for i in tmp:
    rh = i.medicine_str
    med_l = rh.split('&&&')
    for j in med_l[:-1]:
        med = j.split('___')
        medname = med[0]
        medbatch = med[1]
        medno = med[2]
        print i, med
        tmp_tab = tablets.objects.filter(tag__name=medname,batch_no=medbatch)[0]
        tmp_item = invoiceitem(tab=tmp_tab, nitems=int(medno))
        tmp_item.save()
        i.tab.add(tmp_item)
        i.save()
