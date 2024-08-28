from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.sessions.models import Session
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .basket import *
from store.models import * 
from .models import *
from django.db.models import F, Sum
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
# Create your views here.


    

def list_basket_view(request):
    user = request.user if request.user.is_authenticated else None
    
    if  not user:   
        
        basket = Basket(request)
 
    else:
        
        basket = UserBasket(request)
    # for item in basket.total_price():
    #     print(item)
    return render(request,'basket/shopping-cart.html',{'basket':basket})

  
def add_basket_view(request):
    basket = None
    data = None
    total_qty = 0
    if request.method == 'POST':
        # GETTING FROM TEMPLATE
        product_slug = request.POST.get('product_slug')
        C_id = request.POST.get('color')
        S_id = request.POST.get('size')
        _qty = int(request.POST.get('product_qty')) 

        _product = SubProduct.objects.get(product__slug=product_slug,color=C_id,size=S_id)
        user = request.user if request.user.is_authenticated else None

        if  not user:
            basket = Basket(request)
            data=basket.add(_product.id,_qty)
            total_qty = basket.len()
            
        else:
            basket = UserBasket(request)
            data=basket.add(_product,_qty)
            total_qty = basket.len()
            
      

        if data:
            message = 'Item(s) Successfully Added!'
        else:
            message = 'Somethings is wrong!'
       
        return  JsonResponse({'qty':total_qty,'message':message,'get_sub_total':str(basket.total_amount())})
    

def edit_basket_view(request):
    basket = None
    data = None
    total_qty = 0
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        qty = request.POST.get('product_qty')
       
        if product_id:
            product = get_object_or_404(SubProduct,id=product_id)
        user = request.user if request.user.is_authenticated else None
        if  not user:
            basket = Basket(request)
            data = basket.edit(product,qty)

        else:
            basket = UserBasket(request)
            data = basket.edit(product,qty)
           

        if data:
            message = 'Cart successfully updated!'
        else:
            message = 'Something is Wrong!'
    
        content = {'product_id':str(product.id),'message':message,'data':data,}
        return  JsonResponse(content)


def remove_basket_view(request):    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(SubProduct,id=product_id)
       

        if(product):
            user = request.user if request.user.is_authenticated else None
            if  not user:
                  basket = Basket(request)
                  basket.delete(product)
            else:
                basket = UserBasket(request)
                basket.delete(product)

        messages.info(request,'Item Remove successfully')
       
        return redirect("/")


@login_required
def list_wishlist_view(request):
    # wishlist = WishList.objects.filter(account=request.user)
    # return render(request,'basket/wishlist.html',{'wishlist':wishlist})
    return render(request,'basket/wishlist.html')
 

@login_required
def add_wishlist_view(request):
    message, count = None , 0
    
    if request.user.is_authenticated == True:
        if request.method == 'POST':
            product_slug = request.POST.get('product_slug')
            C_id = request.POST.get('color')
            S_id = request.POST.get('size')
            variant  = SubProduct.objects.get(product__slug=product_slug,color=C_id,size=S_id)      
            
            wishlist = WishList.objects.filter(account=request.user,product=variant)
            if wishlist.exists() == False:
                wishlist = WishList(account=request.user,product=variant)
                wishlist.save() 
                if wishlist:
                    message = 'ADDED IN WISHLIST'
                    count = WishList.objects.filter(account=request.user).count()
                    wishlisk_chk = True 
                else:
                    message = 'SOMETHING IS WRONG'  
            else:
                wishlist = wishlist.delete()
                if wishlist:
                    message = 'REMOVE FROM WISHLIST'
                    count = WishList.objects.filter(account=request.user).count()
                    wishlisk_chk = False
    
                else:
                    message = 'SOMETHING IS WRONG'
    else:
        message = 'LOGIN REQUIRED FOR WISHLIST'
    return JsonResponse({'message':message,'count':count,'wishlist_chk':wishlisk_chk})




@login_required
def remove_wishlist_view(request):
    product_id = request.POST.get('product_id')
    wishlist = WishList.objects.filter(account=request.user,product=product_id)
    wishlist = wishlist.delete()
    if wishlist:
        message = 'REMOVE FROM WISHLIST'
    else:
        message = 'SOMETHING IS WRONG'
    return JsonResponse({'message':message})