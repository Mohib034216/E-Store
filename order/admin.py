from django.contrib import admin
from .models import *

# Register your models here.


# class OrderStatusAdmin(admin.ModelAdmin):
#     list_display = ['status']
   
# admin.site.register(OrderStatus,OrderStatusAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','total_amount','order_status',]
    list_editable = ['order_status']
   
admin.site.register(Order,OrderAdmin)
# admin.site.register(ShoppingCart)