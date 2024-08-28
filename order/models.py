from django.db import models
from account.models import Account, AddressBook
from payments.models import *

from store.models import Product, SubProduct
# Create your models here.

# class ShippingMethod(models.Model):
#     name = models.CharField( max_length=50)
#     price = models.IntegerField()
    
# class OrderStatus(models.Model):
#     status = models.CharField(max_length=15)

#     def __str__(self):
#        return  str(self.status)




# order table  not migrate some error here 


# class OrderManager(models.Manager):
#     def create_or_update_order(self, user, total_price, **kwargs):
#         defaults = {
#             'total_price': total_price,
#             **kwargs
#         }
#         order, created = self.update_or_create(user=user, defaults=defaults)
#         return order, created


class Order (models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_address  = models.ForeignKey(AddressBook,related_name='billing_address',on_delete=models.SET_NULL,blank=True, null=True)
    shipping_address = models.ForeignKey(AddressBook,related_name='shipping_address',on_delete=models.SET_NULL,blank=True, null=True)
    payment = models.ForeignKey(PaymentMethod,null=True,on_delete = models.CASCADE)
    # shipping_method = models.ForeignKey(ShippingMethod,on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    ORDER_STATUS = (
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
        ('archived', ('Archived - not available anymore')),
    )
    order_status = models.CharField(choices=ORDER_STATUS, max_length=200,default='Processing')
    ordered_at  = models.DateTimeField(auto_now_add=True)
    ordered_approved_at  = models.DateTimeField(blank=True,null=True)
    ordered_delivered_carrier_at  = models.DateTimeField(null=True, blank=True)
    ordered_delivered_customer_at  = models.DateTimeField(null=True, blank=True)

    # obj = OrderManager()
    # objects = models.Manager()

    class Meta:
        verbose_name = "ShoppingOrder"
        verbose_name_plural = "ShoppingOrder"

    def __str__(self):
       return  str(self.pk)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product   = models.ForeignKey(SubProduct, on_delete=models.CASCADE)
    price  =  models.DecimalField(max_digits=10, decimal_places=2)
    quantity   = models.IntegerField(default=1)

    class Meta:
        verbose_name = "ShoppingOrderItem"
        verbose_name_plural = "ShoppingOrderItems"

    
    
    
    

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


# class Refund(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     reason = models.TextField()
#     accepted = models.BooleanField(default=False)
#     email = models.EmailField()

#     def __str__(self):
#         return f"{self.pk}"
