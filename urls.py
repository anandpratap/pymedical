from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from settings import STATIC_ROOT, STATICFILES_DIRS
urlpatterns = patterns('',
                       # Examples:
                           # url(r'^$', 'medical.views.home', name='home'),
                       # url(r'^medical/', include('medical.foo.urls')),
                       
                       # Uncomment the admin/doc line below to enable admin documentation:
                           # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin:
                           (r'^static/(?P<path>.*)$', 'django.views.static.serve',{\
            'document_root': STATIC_ROOT}),  
                       
                       url(r'^admin/', include(admin.site.urls)),
#                       url(r'^simple-autocomplete/', include('simple_autocomplete.urls')) ,
                       (r'^$', 'account.views.addinvoice'),
                       (r'^process/', 'account.views.readform'),
                       (r'^eprocess/', 'account.views.ereadform'),
                       (r'^stock_add/$', 'account.views.addstock'),
                       (r'^medicine_add/', 'account.views.addmedicine'),
                       (r'^firm_add/', 'account.views.addfirm'),
                       (r'^type_add/', 'account.views.addtype'),    
                       (r'^pharma_add/', 'account.views.addpharma'),    
                       (r'^stock_add_process/', 'account.views.addstockprocess'),
                       (r'^medicine_add_process/', 'account.views.addmedicineprocess'),
                       (r'^firm_add_process/', 'account.views.addfirmprocess'),
                       (r'^type_add_process/', 'account.views.addtypeprocess'),
                       (r'^pharma_add_process/', 'account.views.addpharmaprocess'),
                       (r'^dash/', 'account.views.dash'),
                       (r'^stock_view/', 'account.views.viewstock'),
                       (r'^credit_view/', 'account.views.viewcredit'),
                       
                       (r'^stock_edit/(?P<pid>\d+)/$', 'account.views.editstock'),
                       (r'^stock_delete/(?P<pid>\d+)/$', 'account.views.deletestock'),
                       (r'^stock_edit_process/', 'account.views.editstockprocess'),
                       (r'^search/', 'account.views.searchlist'),
                       (r'^searchp/', 'account.views.searchlist_patient'),
                       (r'^credit_view_details/(?P<pid>\d+)/$', 'account.views.viewcreditdetails'),
                       (r'^invoice_view/(?P<pid>\d+)/$', 'account.views.viewinvoice'),
                       (r'^invoice_edit/(?P<pid>\d+)/$', 'account.views.editinvoice'),
                       (r'^invoice_print/(?P<pid>\d+)/$', 'account.views.printinvoice'),
                       #(r'^invoice_search/(?P<pid>\d+)/$', 'account.views.searchinvoice'),
                       (r'^add_credit_amount/$', 'account.views.addcreditamount'),
                       (r'^expiry_view/$', 'account.views.viewexpiry'),
                       (r'^demand_view/$', 'account.views.viewdemand'),
                       (r'^stats/', 'account.secview.statistics'),
                       
                       ( r'^ajax/', include( 'account.urls' ) ),
                       
                       (r'^pdfstock/', 'account.secview.latex_total_stock_str'),
                       (r'^pdfdemand/', 'account.secview.pdfdemand'),
                       (r'^visual/', 'account.plots.plots'),
                       (r'^logout/', 'account.auth.logoutprocess'),
                       (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
            (r'^loginprocess/', 'account.auth.loginprocess'),
                       )
