from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.checkoutform,name="checkoutform"),
    path('edit',views.edit_checkoutform,name="editcheckoutform"),
    path('order_placed/',views.placedorder,name="success-order"),
    # path('detail/<slug:slug>',views.detailproduct,name="detailproduct"),

    
]
