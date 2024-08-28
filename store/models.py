from ast import keyword, mod
from email.policy import default
from random import choices
from sre_constants import MAX_UNTIL
from turtle import title
from unicodedata import category
from unittest.mock import DEFAULT
from django.db import models
# from mptt.models import MPTTModel,TreeForeignKey
from tinymce import models as tiny_models
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.urls import reverse 
from treebeard.mp_tree import MP_Node

import uuid
# Create your models here.

# class Category(MPTTModel):

#     CATEGORY_TYPE = (
#         ('parent','parent'),
#         ('child','child'),
#         ('subchild','subchild'),
#     )
#     parent      = TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
#     title       = models.CharField(max_length=30)
#     type        = models.CharField(max_length=30,default='parent',choices=CATEGORY_TYPE)
#     keywords    = models.CharField(max_length=255,blank=True,null=True)
#     slug        = models.SlugField( unique=True)
#     is_active   = models.BooleanField(default=True)
#     created_at  = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_at  = models.DateTimeField(auto_now_add=False,auto_now=True)

    
#     class Meta:
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
   
#     # def __str__(self):
#     #     return self.title

#     class MPTTMeta:
#         order_insertion_by = ['title']

#     def __str__(self) :
#         full_path = [self.title]
#         k = self.parent
#         while k is not None:
#             full_path.append(k.title)
#             k = k.parent
#         return '/'.join(full_path[::-1])
 
#     def all_category(self):
#         return self.objects.all()

class Category(MP_Node):
    CATEGORY_TYPE = (
        ('parent','parent'),
        ('child','child'),
        ('subchild','subchild'),
    )
    # parent      = TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    title       = models.CharField(max_length=30)
    type        = models.CharField(max_length=30,default='parent',choices=CATEGORY_TYPE)
    keywords    = models.CharField(max_length=255,blank=True,null=True)
    slug        = models.SlugField( unique=True)
    image       = models.ImageField(upload_to='category_images/',null=True,blank=True)
    is_active   = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_at  = models.DateTimeField(auto_now_add=False,auto_now=True)

    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return 'Category: {}'.format(self.title)

    # class MPTTMeta:
    #     order_insertion_by = ['title']

    # def __str__(self) :
    #     full_path = [self.title]
    #     k = self.parent
    #     while k is not None:
    #         full_path.append(k.title)
    #         k = k.parent
    #     return '/'.join(full_path[::-1])
 
    def all_category(self):
        return self.objects.all()
        
class Brand (models.Model):
    title       = models.CharField(max_length=50,default='None')
    image       = models.ImageField(upload_to='brand_images/',null=True,blank=True) 
    description = tiny_models.HTMLField(default='This is new store')
    is_active   = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now=False,auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def brand_image(self):
        return format_html('<img src="{}" width=75 height=70 />'.format(self.image.url))


class Product(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    title       = models.CharField( max_length=150)
    keywords    = models.CharField(max_length=255,blank=True,null=True)
    price       = models.DecimalField( max_digits = 8, decimal_places = 2,default=0)
    description = tiny_models.HTMLField()
    brand       = models.ForeignKey(Brand,null=True,blank=True,default='None',on_delete=models.CASCADE)
    slug        = models.SlugField(unique=True)
    is_featured = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=False)
    # image       =  models.ImageField(upload_to='product_images/',null=True,blank=True) 
    created_at  = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_at  = models.DateTimeField(auto_now_add=False,auto_now=True)
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):    
        return reverse('detail', args=[str(self.slug),str(self.init_variant().sku)])

    def product_image(self,):
        return format_html('<img src="{}" width=75 height=70 />'.format(self.image.url))
    
    def img(self):
        img = Media.objects.filter(subproduct=SubProduct.objects.filter(product=self.id).first()).first()
        return img

    def init_variant(self):
        return SubProduct.objects.filter(product=self.id).first()
   
    # def variants(self):
    #     return SubProduct.objects.filter(product=self.id)
   



class Size (models.Model):
    title       = models.CharField(max_length=100)
    code        = models.CharField(max_length=50,null=True,blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now=False,auto_now_add=True)
    
    def __str__(self):
        return str(self.title)

    
class Color (models.Model):
    title       = models.CharField(max_length=100)
    code        = models.CharField(max_length=50,null=True,blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return str(self.title)

    def color(self):
        return format_html('<b style="background:{};">{}</b>'.format(self.title,self.title))



class SubProduct(models.Model):
    product       = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='subproducts')
    color         = models.ForeignKey(Color,null=True,blank=True,on_delete=models.CASCADE)
    size          = models.ForeignKey(Size,null=True,blank=True,on_delete= models.CASCADE)
    sku           = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    stock_price   = models.DecimalField(max_digits = 8, decimal_places = 2,default=0)    
    retail_price  = models.DecimalField( max_digits = 8, decimal_places = 2,default=0)    
    sale_price    = models.DecimalField( max_digits = 8, decimal_places = 2,default=0)    
    stock_qty     = models.IntegerField()
    is_active     = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now=False,auto_now_add=True,null=True,blank=True)
    
  
    def __str__(self):
        product= self.product.title
        return f"{product[:40]} (color: {self.color}) (size: {self.size})" 
    
    def tumbnail(self):
        return Media.objects.filter(subproduct=self.id).first()
        
    def gallery_imgs(self):
        images = Media.objects.filter(subproduct=self.id)
        for img in images:
            return format_html('<img src="{}" width=75 height=70 />'.format(img))
 
    def title(self):
        return self.product.title
    
    def is_stock(self):
        if self.stock_qty > 0:
            return 'In Stock'
        else:
            return 'Out Stock'

  
    def sale_percent(self):
        if self.sale_price > 0:
            return ((self.retail_price - self.sale_price) /self.retail_price) * 100
        
    def get_price(self):
        if self.sale_price > 0 :
            return self.sale_price
        else:
            return self.retail_price
    
    def get_old_price(self):
        if self.sale_price > 0 :
            return self.retail_price
        return ''

class Media (models.Model):
    image       = models.ImageField(upload_to='product_images/') 
    subproduct  = models.ForeignKey(SubProduct,related_name='sub_images',on_delete=models.CASCADE)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return str(self.image.url)


    
  


    