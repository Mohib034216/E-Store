from decimal import Decimal
from sites import settings
from store.models import *
from .models import *
from django.shortcuts import redirect,get_object_or_404
from django.db.models import Sum,F


      


class Basket():
 """BASKET FOR WHEN NON-USER/GUEST VISIT """

 def __init__(self,request):
    self.session = request.session
    basket = self.session.get(settings.CART_SESSION_KEY)
    if settings.CART_SESSION_KEY not in request.session:
        basket = self.session[settings.CART_SESSION_KEY] = {}
    self.basket = basket

 def len(self):
   qty = sum(int(item['qty']) for item in self.basket.values())
   return qty
 

 def view(self):
      basket      = self.basket
      for item in basket.values():
         product = SubProduct.objects.get(id=item['product_id'])
         item['total_price'] = float(product.sale_price) * int(item['qty'])  
         # yield product
         yield {'product':product,'item':item}


 
 def add(self,_pk,_qty):
      if  'product_%s'%(_pk) in self.basket:
         _qty = int(self.basket['product_%s'%(_pk)]['qty']) + _qty
         self.basket['product_%s'%(_pk)]['qty'] =str(_qty)
         result = self.session.modified =True
         
      else:  
         self.basket['product_%s'%(_pk)]= {'product_id':str(_pk),'qty':str(_qty)}
         result = self.session.modified = True
      if result:
         return True   
      return False
   



 def edit(self,product,_qty):
   _pk = product.id
   total_price = float(product.sale_price) * int(self.basket['product_%s'%(_pk)]['qty'])
   if  'product_%s'%(_pk) in self.basket:

      self.basket['product_%s'%(_pk)]['qty'] = str(_qty)
      total_price = float(product.sale_price) * int(self.basket['product_%s'%(_pk)]['qty'])  
      self.session.modified =True
   return {'total_qty':self.len(),'total_price':str("{:.2f}".format(total_price)),'gross_amount':str(self.gross_amount()),'total_amount':str(self.total_amount())}
        

 
 def delete(self,product):
   _pk = product.id
   del self.basket['product_%s'%(_pk)]  
   self.session.modified =True


 def gross_amount(self):
      basket     = self.basket
      price = SubProduct.objects.filter(id__in=[item['product_id'] for item in basket.values()]).values_list('sale_price',flat=True)
      qty =  [item['qty'] for item in basket.values()]
      # print(price)
      result = []
      for i in range(0, len(qty)):
         result.append(int(qty[i]) * price[i])

      gross_amount = sum(result)
      return gross_amount
 
 def total_amount(self):
      basket     = self.basket
      price = SubProduct.objects.filter(id__in=[item['product_id'] for item in basket.values()]).values_list('sale_price',flat=True)
      qty =  [item['qty'] for item in basket.values()]
      result = []
      for i in range(0, len(qty)):
         result.append(int(qty[i]) * price[i])
      total_amount = sum(result)
      return total_amount
     
 




class UserBasket():
    """ BASKET FOR WHEN USER LOGIN """


    def __init__(self,request):
        global user
        user = request.user
    
         
    def view(self):
        result = ShoppingCartItem.objects.filter(shoppingcart__account = user).annotate(total_price=F('qty')* F('product__sale_price'))
        return result
    
    def total_price(self):
      total = 0
      product   =  ShoppingCartItem.objects.filter(shoppingcart__account = user)
      for item in product:
         total += float(item.product.sale_price) * int(item.qty)  
         # yield item
      return total
       
       
    def add(self,product,_qty):
      if  user:
         cart_item = None
         try:
            cart_item  = ShoppingCartItem.objects.get(shoppingcart__account = user ,product=product.id)
   
            if  cart_item:
               cart_item.qty += _qty
               cart_item.save()
               return True
         except :
            cart_item = ShoppingCartItem(product=product,qty=_qty,is_active=True)
            cart_item.save()

            if  cart_item:
               user_cart = ShoppingCart(account=user,cart=cart_item)
               user_cart.save()
               return True
         return False
 

   #  def __len__(self):
   #    if  user:
   #       qty =  ShoppingCartItem.objects.filter(shoppingcart__account=user.id).values('qty').aggregate(qty=Sum('qty'))
   #       return qty
  
     
    def len(self):
        if  user:
         qty = sum(item['qty'] for item in ShoppingCartItem.objects.filter(shoppingcart__account=user.id).values('qty'))
         
         return int(qty)


    def edit(self,product,_qty):
      if  user:

         try:
            cart_item  = ShoppingCartItem.objects.get(shoppingcart__account=user,product=product.id)
            if  cart_item:
               cart_item.qty = _qty
               cart_item.save()
           
         except :
            total_price = 0
            cart_item = None
         total_price = int(cart_item.qty) * float(cart_item.product.sale_price)
   
         return {'total_qty':int(self.len()),'total_price':str("{:.2f}".format(total_price)),'gross_amount':str(self.gross_amount()),'total_amount':str(self.total_amount())}
                     
 
    def delete(self):
      if  user:
         cart_item = ShoppingCart.objects.filter(account=user).delete()
     

    def gross_amount(self):
      if  user:
         result = []
         for val in  self.view():
            result.append(val.total_price)
         return sum(result)
 
    def total_amount(self):
      if  user:
         result = []
         for val in  self.view():
            result.append(val.total_price)
         return sum(result)
      
   
    def cart_is_empty(request):
    #   if request.user.is_authenticated:
        user = request.user  # Assuming you have user authentication
        cart_items = ShoppingCart.objects.filter(account=user)
        return not cart_items.exists()
      