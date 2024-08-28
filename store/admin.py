from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import *
# Register your models here.
# from mptt.admin import DraggableMPTTAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Category
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CategoryAdmin(TreeAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = movenodeform_factory(Category)
   

admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ['title','brand_image','is_active']
    list_editable = ['is_active']
   

admin.site.register(Brand, BrandAdmin)

# class CategoryAdmin(DraggableMPTTAdmin):
#     mptt_indent_field = "name"
#     list_display = ('tree_actions', 'indented_title',
#                     'related_products_count', 'related_products_cumulative_count')
#     list_display_links = ('indented_title',)
#     prepopulated_fields = {'slug': ('title',)}
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)

#         # Add cumulative product count
#         qs = Category.objects.add_related_count(
#                 qs,
#                 Product,
#                 'category',
#                 'products_cumulative_count',
#                 cumulative=True)

#         # Add non cumulative product count
#         qs = Category.objects.add_related_count(qs,
#                  Product,
#                  'category',
#                  'products_count',
#                  cumulative=False)
#         return qs

#     def related_products_count(self, instance):
#         return instance.products_count
#     related_products_count.short_description = 'Related products (for this specific category)'

#     def related_products_cumulative_count(self, instance):
#         return instance.products_cumulative_count
#     related_products_cumulative_count.short_description = 'Related products (in tree)'
    

# admin.site.register(Category,CategoryAdmin)

class RequireOneFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if not self.is_valid():
            return
        if not self.forms or not self.forms[0].cleaned_data:
            raise ValidationError('At least one {} required'
                                  .format(self.model._meta.verbose_name))
        
    

class ProductImagesInline(admin.TabularInline):
    model = Media
    formset =  RequireOneFormSet
    
        
class SubProductInline(admin.TabularInline):
    model = SubProduct
    
    formset =  RequireOneFormSet
    inlines = [
        ProductImagesInline
        ]
   
class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['title','keywords','price','is_featured','is_active']
    prepopulated_fields = {'slug': ('title',)}
    list_editable=['is_featured','is_active']
    inlines = [
        SubProductInline
    ]

admin.site.register(Product,ProductAdmin)

class SubProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','product','gallery_imgs','color','size','stock_price','retail_price','sale_price','stock_qty','created_at','is_active']
    # prepopulated_fields = {'slug': ('product','color','size',)}
    inlines = [
        ProductImagesInline
        ]
    list_editable=['is_active'] 
    # prepopulated_fields = {'slug': ('title',)}

admin.site.register(SubProduct,SubProductAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display = ['id','color','created_at','is_active']
    list_editable=['is_active'] 

admin.site.register(Color,ColorAdmin)


class SizeAdmin(admin.ModelAdmin):
    list_display = ['id','title','created_at','is_active']
    list_editable=['is_active'] 

admin.site.register(Size,SizeAdmin)

admin.site.register(Media)



