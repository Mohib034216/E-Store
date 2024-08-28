from django.urls import path
from django.contrib.auth import views as   auth_views
from . import views
from .form import (UserLoginForm)

app_name = 'account'
    
urlpatterns = [
    path('login',auth_views.LoginView.as_view(template_name='account/sign-in.html',next_page='/',form_class=UserLoginForm),name="sign_in"),
    path('logout',auth_views.LogoutView.as_view(next_page='account:sign_in'),name="logout"),
    path('register',views.register,name="user_register"),
    path('dashboard',views.dashboard_view,name="user_dashboard"),


    path('form/addressbook',views.address_form_view,name="addressform"),
    path('addressbook',views.get_user_address_view,name="user_address"),
    path('add/addressbook',views.set_user_address_view,name="set_user_address"),
    # path('edit/addressbook',views.update_user_address_view,name="update_user_address"),
    path('addressbook/del',views.address_delete_view,name="address_delete_view"),
    path('activate/<slug:uidb64>/<slug:token>/',views.account_activate,name="activate"),
    
    path('user-addressbook',views.list_address,name="list_useraddress"),



  ]
