from account.models import*
from django.contrib import admin
class tabletsAdmin(admin.ModelAdmin):
    list_display = ('tag', 'batch_no','printed_price','actual_price')
    search_fields = ['tag__name']
    list_filter = ['purchased_date']
    def has_add_permission(self, request):
        return False
class medicineAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
    def has_add_permission(self, request):
        return False



admin.site.register(medicinetype)
admin.site.register(medicinefirm)
admin.site.register(medicine,medicineAdmin)
admin.site.register(tablets, tabletsAdmin)
admin.site.register(pharmashop)
admin.site.register(invoice)
admin.site.register(invoiceitem)
admin.site.register(patient)
admin.site.register(purchase)
admin.site.register(dateobject)
admin.site.register(creditobject)


