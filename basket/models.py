from django.db import models
from account.models import Account

from store.models import Product, SubProduct

# Create your models here.


class ShoppingCartItem(models.Model):
    product = models.ForeignKey(SubProduct, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    is_active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "ShoppingCartItem"
        verbose_name_plural = "ShoppingCartItems"

    # def get_price():
    #     return self.product.get_price

    def get_total_price(self):
        return float(self.product.get_price()) * int(self.qty) 

class ShoppingCart(models.Model):
    account = models.ForeignKey(Account,
             on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCartItem,
             on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "ShoppingCart"
        verbose_name_plural = "ShoppingCarts"

    def __str__(self):
       return  self.Account.username
    

  
    
class WishList(models.Model):
    account = models.ForeignKey(Account,
             on_delete=models.CASCADE)
    product = models.ForeignKey(SubProduct,
             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
  

    class Meta:
        verbose_name = "WishLists"
        verbose_name_plural = "WishLists"

    # def __str__(self):
    #    return  str(self.account)
    
    # def wishlist(self):
    #     return self.objects.filter(account=self.user)
