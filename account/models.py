from django.db import models
from django import forms
# Create your models here.
import os

class medicinetype(models.Model):
    name = models.CharField(max_length=100)
    minno = models.IntegerField(default=0) 
    def __unicode__(self):
        return self.name

class medicinefirm(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
class pharmashop(models.Model):
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    def __unicode__(self):
        return self.name

class medicine(models.Model):
    name = models.CharField(max_length=100)
    medicinetype = models.ForeignKey(medicinetype, blank=False, null=False)
    medicinefirm = models.ForeignKey(medicinefirm, blank=False, null=False)
    def __unicode__(self):
        return self.name
class patient(models.Model):
    name = models.CharField(max_length=1000)
    telephone = models.CharField(max_length=15)
    credit_paid = models.CharField(max_length=10)
    balance = models.CharField(max_length=10, default='')
    credit_history = models.TextField(max_length=100000)

    def __unicode__(self):
        return self.name +" "+ self.telephone


        


#Rename tablets as units
class tablets(models.Model):

    tag = models.ForeignKey(medicine, blank=False, null=False)
    expiry_date = models.DateTimeField("Expiry Date")
    purchased_date = models.DateTimeField("Purchased Date")
    batch_no = models.CharField(max_length=20)
    actual_price = models.CharField(max_length=10)
    printed_price = models.CharField(max_length=10)
    navailable = models.IntegerField(default=0)
    nsold = models.IntegerField(default=0)
    vat = models.CharField(max_length=4)
    revision_history = models.TextField(max_length=100000)
    pharma_shop = models.ForeignKey(pharmashop, blank=False, null=False)
    def __unicode__(self):
        return self.tag.name + " " + self.batch_no
    def _sale(self, quant):
        self.nsold += quant
        self.navailable -= quant
        self.save()

class dateobject(models.Model):
    date = models.DateTimeField("Date")
    def __unicode__(self):
        return self.date.ctime()
class purchase(models.Model):
    tab = models.ForeignKey(tablets, blank=False, null=False)
    nitems = models.IntegerField(default=0)
    pharmashop = models.ForeignKey(pharmashop, blank=False, null=False)
    date = models.ForeignKey(dateobject, blank=False, null=False)


class invoiceitem(models.Model):
    tab = models.ForeignKey(tablets, blank=False, null=False)
    nitems = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.tab.tag.name
    def additem(self, n):
        self.nitems += n
        self.save()


class invoice(models.Model):
    date = models.ForeignKey(dateobject, blank=False, null=False)
    tab = models.ManyToManyField(invoiceitem)
    invoice_no = models.CharField(max_length=10)
    patient = models.ForeignKey(patient, blank=False, null=False)
    invoice_date = models.CharField(max_length=20)
    total = models.CharField(max_length=20)
    paid = models.CharField(max_length=20)
    nmedicine = models.IntegerField(default=1)
    medicine_str = models.CharField(max_length=10000)
    date_created = models.DateTimeField("Date Created")
    date_last_modified = models.DateTimeField("Date Last Modified")
    revision_history = models.TextField(max_length=100000)
    is_delete = models.BooleanField(default=False)
    def __unicode__(self):
        return self.invoice_no

class creditobject(models.Model):
    amount = models.CharField(max_length=10)
    date = models.ForeignKey(dateobject, blank=False, null=False)
    patient = models.ForeignKey(patient, blank=False, null=False)
    def __unicode__(self):
        return self.patient.name

class stockform(forms.Form):
    tag_name = forms.CharField(max_length=100)
    batch_no = forms.CharField(max_length=20)
    expiry_date = forms.DateTimeField()
    actual_price = forms.CharField(max_length=100)
    printed_price = forms.CharField(max_length=100)
    vat = forms.CharField(max_length=100)
    pharma_shop = forms.CharField(max_length=100)
    nmedicine = forms.CharField(max_length=10)

class medicineform(forms.Form):
    tag_name = forms.CharField(max_length=100)
    firm = forms.CharField(max_length=100)
    mtype = forms.CharField(max_length=100)

class medicinetypeform(forms.Form):
    tag_name = forms.CharField(max_length=100)
    
class medicinefirmform(forms.Form):
    tag_name = forms.CharField(max_length=100)
   
class pharmaform(forms.Form):
    tag_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
class search_form(forms.Form):
    query = forms.CharField(max_length=1000)

class credit_form(forms.Form):
    pid = forms.CharField(max_length=100)
    amount = forms.CharField(max_length=1000)
class expiry_form(forms.Form):
    query = forms.CharField(max_length=1000)

