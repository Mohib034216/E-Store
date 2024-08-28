from basket.basket import Basket, UserBasket
from store.models import Category
from basket.models import WishList


def categories(request):
    root_categories = Category.get_root_nodes()

    context = {'root_categories':root_categories}
    return context


def basket(request):
    user = request.user if request.user.is_authenticated else None
    if not user:
        return {'basket':Basket(request)}
    else:
        basket = UserBasket(request)
        wishlist = WishList.objects.filter(account=user)
        if hasattr(request, 'resolver_match'):
            sku = request.resolver_match.kwargs.get('sku')
            chk_ = wishlist.filter(product__sku=sku).exists()
            
        return {'basket':basket,'wishlist':wishlist,'wishlist_chk':chk_}
    
