from django.contrib import admin
from django.urls import path
from . import views
import uuid

urlpatterns = [
    path('',views.testedhome_view,name="home_test"),
    path('detail/<uuid:sku>',views.tested_view,name="tested"),
   

    
]
