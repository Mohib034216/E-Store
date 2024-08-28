from django.shortcuts import redirect
from basket.basket import *




def cart_not_empty_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user's cart is empty (you need to implement this logic)
        if UserBasket.cart_is_empty(request):
            return redirect('shop')  # Redirect to the shop page if the cart is empty
        else:
            return view_func(request, *args, **kwargs)  # Proceed to the checkout form

    return _wrapped_view