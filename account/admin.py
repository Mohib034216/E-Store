from django.contrib import admin
from .models import Account,AddressBook
# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ['username','email','phone','created_at','is_active']
    list_editable=['is_active'] 
    # prepopulated_fields = {'slug': ('title',)}

admin.site.register(Account,AccountAdmin)

class AddressBookAdmin(admin.ModelAdmin):
    list_display = ['title','address_line_1','created_at','is_active']
    list_editable=['is_active'] 
    # prepopulated_fields = {'slug': ('title',)}

admin.site.register(AddressBook,AddressBookAdmin)
