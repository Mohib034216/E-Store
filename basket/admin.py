from django.contrib import admin
from .models import *
# Register your models here.

class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ['product','qty','updated_at','created_at','is_active']
   
admin.site.register(ShoppingCartItem,ShoppingCartItemAdmin)
admin.site.register(ShoppingCart)