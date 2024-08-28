from django.contrib import admin
from payments.models import *
# Register your models here.

class PaymentMethodsAdmin(admin.ModelAdmin):
    list_display = ['amount', 'paymenttype','provider','account_number','expiry_date','is_default' ,'created_at']   

class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['value']   
    
admin.site.register(PaymentMethod,PaymentMethodsAdmin)
admin.site.register(PaymentType,PaymentTypeAdmin)
# admin.site.register(ShoppingCart)