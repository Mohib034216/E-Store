from django.shortcuts import render,redirect,get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from account.form import AddressUserForm
from django.db.models import F, Sum
from account.models import *
from basket.models import *
from .models import *
from basket.basket import Basket, UserBasket
from order.checkout import Checkout
from order.Decorators import *
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse

# Create your views here.


@login_required 
@cart_not_empty_required
def placedorder(request):
        basket = UserBasket(request)
        checkout = Checkout(request)
        if request.method == 'POST':
            if checkout.billing and checkout.shipping:
                payment_type = request.POST.get('paymentMethod')
                if payment_type:
                    paymenttype = PaymentType.objects.get(pk=payment_type)
                    # order = Order(user=Account.objects.get(id=request.user),total_amount=basket.total_amount(),billing_address=checkout.billing(),shipping_address=checkout.shipping(),payment=payment)
                    paymentmethod = PaymentMethod(amount=basket.total_amount(),paymenttype=paymenttype)
                    paymentmethod.save()
                    order = Order(user=Account.objects.get(id=request.user.id),
                            total_amount=basket.total_amount(),
                            billing_address=checkout.billing(),
                            shipping_address=checkout.shipping(),
                            payment=paymentmethod,is_paid=False)
                    order.save()      
                    for item in  basket.view():
                        # print(f'QTY:{item.qty}')
                        orderitem = OrderItem(order=order,product=item.product,price=item.product.get_price(),quantity=item.qty)
                        # print(item.product)
                        orderitem.save()
                    if orderitem:
                        basket.delete()
                        checkout.delete()
                    return render(request,'order/success-order.html')
            else:
                return JsonResponse({msg:'Add Address'})
        return JsonResponse({msg:'Something Went Wrong '})





                   

# @login_required 
# @cart_not_empty_required
# def checkoutform(request):
#     checkout = Checkout(request)
#     account = Account.objects.get(id=request.user.id)
#     cart    =  ShoppingCart.objects.filter(account=account)
 
#     try:
#         addresses = AddressBook.objects.filter(profile=account)
#         if addresses:
#             data = {'shipping':addresses.filter(ship_default=True).first().id,'billing':addresses.filter(bill_default=True).first().id}    
#             address_instance = checkout.add(account.id,data)
           
#             return render(request, 'order/checkout_form.html',{'address_instance':address_instance})
#         else:
#             return render(request, 'order/checkout_form.html')
#     except AddressBook.DoesNotExist:
#         return render(request, 'order/checkout_form.html')

    # return render(request, 'order/checkout_form.html', {'address_instance':address_instance,'addresses':addresses})

 

@login_required 
@cart_not_empty_required
def checkoutform(request):
    account = Account.objects.get(id=request.user.id)
    # cart    =  ShoppingCart.objects.filter(account=account)
 
    checkout = Checkout(request)
    try:
        addresses = AddressBook.objects.filter(profile=account)
        if addresses:
            data = {'shipping':addresses.filter(ship_default=True).first().id,'billing':addresses.filter(bill_default=True).first().id}    
            address_instance = checkout.add(account.id,data)
            payment = PaymentType.objects.all()
            # print(f'CHECKOUT PAYMENT option{payment}')
            data = {'billing':checkout.billing(),'shipping':checkout.shipping(),'paymethods':payment}
            
            return render(request, 'order/checkout_form.html',data)
        
    except AddressBook.DoesNotExist:
        return render(request, 'order/checkout_form.html')
    return render(request, 'order/checkout_form.html')


@login_required 
@cart_not_empty_required
def edit_checkoutform(request):
    account = Account.objects.get(id=request.user.id)
    ship = request.GET.get('ship')
    bill = request.GET.get('bill')
    
    try:
        addresses = AddressBook.objects.filter(profile=account)
        if addresses:
            checkout = Checkout(request)
            if ship:
                data = {'shipping':addresses.get(id=ship).id}    
                address_instance = checkout.edit(account.id,data)
                
            elif bill:
                data = {'billing':addresses.get(id=bill).id}    
                address_instance = checkout.edit(account.id,data)
                
            result= render_to_string('order/address-content.html',address_instance)
            return  JsonResponse({'result':result})
       
            
    except AddressBook.DoesNotExist:
        return render(request, 'order/checkout_form.html')
    return render(request, 'order/checkout_form.html')




# @login_required 
# @cart_not_empty_required
# def checkoutform(request):
#     cart  =  ShoppingCartItem.objects.filter(shoppingcart__account=request.user.id)
 
#     account = Account.objects.get(id=request.user.id)
    
#     try:
#         # Try to get the object based on some criteria (e.g., a filter condition)
#         bill_address = AddressBook.objects.get(profile=account,address_type='BL',bill_default=True)
#         ship_address = AddressBook.objects.get(profile=account,address_type='SP',ship_default=True)
   
#     except AddressBook.DoesNotExist:
#         # Handle the case when the object does not exist
#         bill_address = None
#         ship_address = None
#         BCUForm = BillingCustomUserForm()
#         SCUForm = ShippingCustomUserForm()

#     if bill_address:
#         BCUForm = bill_address 
#         SCUForm = ship_address
#         if account and  request.method == 'POST':
#             price = []
#             paymenttype = request.POST['paymentMethod']

#             cart  =  ShoppingCartItem.objects.filter(shoppingcart__account=account)
#             price = [item.get_total_price() for item in cart]
#             total_amount = sum(price)
#             print(f'CART-TOTAL:{total_amount}')

#             if not sameaddress == 'on':

#                 shipping_addressbook = AddressBook.objects.create(profile=account,address_line_1=ship_address,address_line_2=ship_optional_address,postal_code=ship_postal_code,country=ship_country,address_type='SP',is_default=False)
#                 shipping_addressbook.save()

#                 billing_addressbook = AddressBook.objects.create(profile=account,address_line_1=address,address_line_2=optional_address,postal_code=postal_code,country=country,address_type='BL',is_default=True)
#                 billing_addressbook.save()
#             else:
#                 billing_addressbook = AddressBook.objects.create(profile=account,address_line_1=address,address_line_2=optional_address,postal_code=postal_code,country=country,address_type='BL',is_default=True)
#                 billing_addressbook.save()

#                 shipping_addressbook=False
    
#                 # print(f'billing first name:{first_name} & Address{address} AND Shipping first name:{ship_first_name} & Address{ship_address} payment type:{paymenttype}')
    
#             Account.objects.update_or_create(defaults={'first_name':first_name,'last_name':last_name,'optional_email':optional_email,'phone':phone},id=request.user.id,)
            
#             paytype = PaymentType(value=paymenttype)
#             paytype.save()

#             payment = PaymentMethod.objects.create(amount=total_amount,paymenttype=paytype)
#             payment.save()
#             if payment:
#                 if shipping_addressbook:
                
#                         order = Order(user=account,billing_address=billing_addressbook,shipping_address=shipping_addressbook,total_amount=total_amount,payment=payment)                    
#                         order.save()
#                 else:
                    
#                         order = Order(user=account,billing_address=billing_addressbook,total_amount=total_amount,payment=payment)                    
#                         order.save()


#                 for item in cart:
#                     item = item
#                     orderitem  = OrderItem.objects.create(order=order,product=item.product,quantity=item.qty)
#                     orderitem.save()
#                 if orderitem:
#                     cart_items =  ShoppingCartItem.objects.filter(shoppingcart__account=account)
#                     cart_items.delete()
            
#                     if cart_items:
#                         cart =  ShoppingCart.objects.filter(account=account)
#                         cart.delete()
#                     return redirect('order_placed/')
                
#     else:
        
#         if account and request.method == 'POST':
#             BCUForm = BillingCustomUserForm(request.POST)
        
#             price = []
#             cart  =  ShoppingCartItem.objects.filter(shoppingcart__account=account)
#             price =  price = [item.get_total_price() for item in cart]
#             total_amount = sum(price)

#             sameaddress = request.POST.get('same_address')

#             if BCUForm.is_valid():
#                     first_name = BCUForm.cleaned_data['first_name']
#                     last_name = BCUForm.cleaned_data['last_name']   
#                     optional_email = BCUForm.cleaned_data['optional_email']
#                     phone = BCUForm.cleaned_data['phone']
#                     country = BCUForm.cleaned_data['country']
#                     address = BCUForm.cleaned_data['address']
#                     optional_address = BCUForm.cleaned_data['optional_address']
#                     postal_code = BCUForm.cleaned_data['postal_code']
#                     paymenttype = request.POST['paymentMethod']

            
#                     if not sameaddress == 'on':
#                         SCUForm = ShippingCustomUserForm(request.POST)
                        
#                         if SCUForm.is_valid():
#                             ship_country = SCUForm.cleaned_data['ship_country']
#                             ship_address = SCUForm.cleaned_data['ship_address']
#                             ship_optional_address = SCUForm.cleaned_data['ship_optional_address']
#                             ship_postal_code = SCUForm.cleaned_data['ship_postal_code']
                        
#                             shipping_addressbook = AddressBook.objects.create(profile=account,address_line_1=ship_address,address_line_2=ship_optional_address,postal_code=ship_postal_code,country=ship_country,address_type='SP',is_default=False)
#                             shipping_addressbook.save()

#                             billing_addressbook = AddressBook.objects.create(profile=account,address_line_1=address,address_line_2=optional_address,postal_code=postal_code,country=country,address_type='BL',is_default=True)
#                             billing_addressbook.save()
#                     else:
#                             billing_addressbook = AddressBook.objects.create(profile=account,address_line_1=address,address_line_2=optional_address,postal_code=postal_code,country=country,address_type='BL',is_default=True)
#                             billing_addressbook.save()

#                             shipping_addressbook=False
#                     Account.objects.update_or_create(defaults={'first_name':first_name,'last_name':last_name,'optional_email':optional_email,'phone':phone},id=request.user.id,)
                    
#                     paytype = PaymentType(value=paymenttype)
#                     paytype.save()

#                     payment = PaymentMethod.objects.create(amount=total_amount,paymenttype=paytype)
#                     payment.save()
#                     if payment:
#                         if shipping_addressbook:
                        
#                                 order = Order(user=account,billing_address=billing_addressbook,shipping_address=shipping_addressbook,total_amount=total_amount,payment=payment)                    
#                                 order.save()
#                         else:
                            
#                                 order = Order(user=account,billing_address=billing_addressbook,total_amount=total_amount,payment=payment)                    
#                                 order.save()


#                         for item in cart:
#                             item = item
#                             orderitem  = OrderItem.objects.create(order=order,product=item.product,quantity=item.qty)
#                             orderitem.save()
#                         if orderitem:
#                             cart_items =  ShoppingCartItem.objects.filter(shoppingcart__account=account)
#                             cart_items.delete()
                    
#                             if cart_items:
#                                 cart =  ShoppingCart.objects.filter(account=account)
#                                 cart.delete()
#                             return redirect('order_placed/')
#         else:
#             BCUForm = BillingCustomUserForm()
#             SCUForm = ShippingCustomUserForm()
#     return render(request, 'order/checkout_form.html', {'billform': BCUForm,'shipform':SCUForm})