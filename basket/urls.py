
from django.urls import path
from django.contrib.auth import views as   auth_views
from . import views

app_name = 'basket'
    
urlpatterns = [
    # URL  ROUTES FOR BASKET | ADD TO CART  
    path('',views.list_basket_view,name="post_basket"),
    path('add_basket',views.add_basket_view,name="add_basket"),
    path('edit_basket',views.edit_basket_view,name="edit_basket"),
    path('remove_basket',views.remove_basket_view,name="remove_basket"),
    
    #URL ROUTES FOR WISHLIST

    path('list_wishlist',views.list_wishlist_view,name="post_wishlist"),
    path('add_wishlist',views.add_wishlist_view,name="add_wishlist"),
    path('remove_wishlist',views.remove_wishlist_view,name="remove_wishlist"),
    
    ]
