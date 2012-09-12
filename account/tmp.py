invoices = invoice.objects.all()
for j in invoices:
    tabs = j.tab.all()
    for k in tabs:
        med = k.tab.tag
        med.consumption_rate += (k.nitems)/float(len(invoices))
        med.save()

