from decimal import Decimal
from sites import settings
from store.models import *
from .models import *
from django.shortcuts import redirect,get_object_or_404
from django.db.models import Sum,F




class Checkout():
 """CHECKOUT FORM """

 def __init__(self,request):
    self._pk = request.user.id
    self.session = request.session
    checkout = self.session.get(settings.CHECKOUT_SESSION_KEY)
    if settings.CHECKOUT_SESSION_KEY not in request.session:
        checkout = self.session[settings.CHECKOUT_SESSION_KEY] = {}
    self.checkout = checkout

 def get(self,_pk):
   checkout     = self.checkout
   if  'user_%s'%(_pk) in checkout:
      data = AddressBook.objects.filter(id__in=[checkout[f'user_{_pk}']['billing'], checkout[f'user_{_pk}']['shipping']])
      return data

 def shipping(self):
   checkout     = self.checkout
   if  'user_%s'%(self._pk) in checkout:
      return AddressBook.objects.get(id=checkout[f'user_{self._pk}']['shipping'])
      

 def billing(self):
   checkout     = self.checkout
   if  'user_%s'%(self._pk) in checkout:
      data = AddressBook.objects.get(id=checkout[f'user_{self._pk}']['billing'])
      return data


 def add(self,_pk,data):
   checkout     = self.checkout
   if  'user_%s'%(_pk) not in self.checkout:
      self.checkout['user_%s'%(_pk)]= data
      result = self.session.modified = True
      if result:
         return self.checkout   
   else:
      return {'billing':self.billing,'shipping':self.shipping}   
 
 
 def edit(self,_pk,data):
   checkout     = self.checkout
   if  'user_%s'%(_pk)  in self.checkout:
      # print(type(data))
      for key,val in data.items():
         print(f'Keys :  {key} values:{val}')
         self.checkout['user_%s'%(_pk)][str(key)]= str(val)
      result = self.session.modified = True
      if result:
         return  {'billing':self.billing(),'shipping':self.shipping()}
   
 def delete(self):
   checkout     = self.checkout
   del self.session[settings.CHECKOUT_SESSION_KEY]
   self.session.modified = True