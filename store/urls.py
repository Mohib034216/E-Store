from django.contrib import admin
from django.urls import path, register_converter
from . import views, converter
import uuid

register_converter(converter.UUIDConverter,'uuid')

urlpatterns = [
    path('',views.shop_list_view,name="shop"),
    path('detail/<slug:slug>-<uuid:sku>',views.get_detail_view,name="detail"),
    path('<slug:slug>',views.get_by_category_view,name="bycategory"),
    path('sorted/<slug:slug>',views.get_by_sort_view,name="bysort"),
    path('search/',views.get_by_search_view,name="search"),

    
]
