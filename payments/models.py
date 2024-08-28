from django.db import models
# from order.models import Order

# Create your models here.

 
# PAYMENT_STATUS = (
#         ('pending','pending'),
#         ('completed','completed'),
#         ('failed','failed'),
#     )

PAYMENT_METHODS =  (
        ('COD','Cash On Delivery'),
        ('CC','Debit/Credit Card'),
        
    )
class PaymentType(models.Model):
    value = models.CharField(choices=PAYMENT_METHODS,max_length=50)

    def __str__(self):
       return  str(self.get_value_display())


class PaymentMethod(models.Model):
    amount = models.FloatField(default=0.0)
    paymenttype = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    provider =  models.CharField( max_length=50,null=True,blank=True)
    account_number = models.IntegerField(null=True,blank=True)
    expiry_date  = models.TextField(null=True,blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)

    
    def __str__(self):
       return  str(self.paymenttype)

