from django.conf.urls.defaults import *
from account.views import *
from account.secview import *
from account.pdf import*
urlpatterns = patterns( '',
                        url( r'^daily/$', send_daily_account, name = 'ajax_daily_account' ),
                        url( r'^monthly/$', send_monthly_account, name = 'ajax_monthly_account' ),
                        url( r'^pdfdaily/$', printdaily, name = 'ajax_daily_latex' ),
                        url( r'^pdfprint/$', printyearly, name = 'ajax_print_latex' ),
                        url( r'^firmstats/$', firmstats, name = 'ajax_firm_stats' ),
                        url( r'^ajaxinvoice/$', readform, name = 'ajax_invoice_process' ),
                        ) 
