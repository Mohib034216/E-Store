from django.shortcuts import render ,redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages 
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode   
from .form import CustomUserForm ,AddressUserForm
from .token import *
from .models import *
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse 
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
import json
from django.core import serializers
from order.models import *
 
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerform = CustomUserForm(request.POST) 

        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.set_password(registerform.cleaned_data['password1'])
            user.is_active = False
            user.save()            
            
            #Email Setup
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account/registration/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                # 'protocol': 'https' if request.is_secure() else 'http',
                
            })
            print(settings.EMAIL_HOST_USER)
            msg = EmailMultiAlternatives(subject,message,settings.EMAIL_HOST_USER,[user.email])
            msg.content_subtype = "html"
            msg.send()
            if msg :
    
                return HttpResponse('Now you need email verification   %s' %(user.email))

        return  HttpResponse('somethings wrong')
    
        
    else:
        
        registerform = CustomUserForm()
        return render(request,'account/sign-up.html',{'form':registerform})


def account_activate(request,uidb64,token):
    user = ''
    try:    
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(id=uid)
    except:
        pass
    if user is not  None and account_activation_token.check_token(user,token):
        user.is_active = True 
        user.save()
        login(request,user)
        if user.is_active == True:
            return redirect('account:user_dashboard')
        
    else:
        return render(request,'account/registration/account_activation_invalid.html',{'user':user,'token':token})


def sign_in(request):
    return render(request,'account/sign-in.html')
    


@login_required    
def dashboard_view(request):
    order = Order.objects.filter(user=request.user.id)
    content = {'order':order}
    return render(request,'account/user/dashboard.html',content)


@login_required    
def get_user_address_view(request):

    addresses   =  AddressBook.objects.filter(profile=request.user,is_active=True)
    addressform =  AddressUserForm()
    if request.method == 'GET' and request.GET.get('address'):
        _pk = request.GET.get('address') 
        
        address = AddressUserForm.get_form_data(_pk)

        addressform =  AddressUserForm(initial=address)
        result= render_to_string('account/user/address-modal-form.html',{'addressform':addressform,'id':_pk})
       
        return  JsonResponse({'result':result})
    
    elif request.method == 'GET' and  request.GET.get('n_addresform'):
        
        result= render_to_string('account/user/address-modal-form.html',{'addressform':addressform})
        return  JsonResponse({'result':result})
    
    content = {'addresses':addresses,'addressform':addressform}
    return render(request,'account/user/address.html',content)




@login_required     
def set_user_address_view(request):
    form = AddressUserForm(request.POST or None)
    _user_address_id = request.POST.get('id')

    if _user_address_id:
        address_instance = get_object_or_404(AddressBook,profile=request.user, id=_user_address_id)
        if request.method == 'POST':
           if form.is_valid():
                fields  = AddressUserForm.address_fields_clean(form)
                user_address = AddressBook.obj.update_addressbook(request.user,address_instance,**fields)
                if user_address:
                    default_fields  =  AddressUserForm.default_fields_clean(form)
                    AddressBook.obj.create_default(request.user,user_address,**default_fields)
    else:
        if request.method == 'POST':
            if form.is_valid():
            
                fields  = AddressUserForm.address_fields_clean(form)
                user_address = AddressBook.obj.create_addressbook(request.user,**fields)

                if user_address:

                    default_fields  =  AddressUserForm.default_fields_clean(form)
                    AddressBook.obj.create_default(request.user,user_address,**default_fields)
            
    return redirect('account:user_address')

@login_required
def address_delete_view(request):
    if request.method == 'GET':
        form_id =   request.GET.get('pk')
        obj  = AddressBook.objects.get(pk=form_id)
        if form_id:
            address_form =  AddressBook.objects.delete_addressbook(obj)
            if address_form:
                AddressBook.objects.create_default(request.user,form_id)

    return JsonResponse({'url':'addressbook'})
       


def address_form_view(request):
    _user_form_id = request.GET.get('pk')

    if _user_form_id:

        obj =  AddressBook.objects.get(id=_user_form_id)
        initial_dict = {'first_name':obj.first_name,'last_name':obj.last_name,'phone':obj.phone,'country':obj.country,'address':obj.address_line_1,'optional_address':obj.address_line_2,'label_tags':obj.title,'ship_default':obj.ship_default,'bill_default':obj.bill_default}
        form =  AddressUserForm(initial = initial_dict)
    else:
        form =  AddressUserForm()
    content = {'form':form}

    return HttpResponse(form)

@login_required
def list_address(request):
    # pass
    data = AddressBook.objects.filter(profile=request.user)

    if request.GET.get('shipping') :
        data = {'shipping':data}
    elif request.GET.get('billing'):
        data = {'billing':data}

    result= render_to_string('account/user/list-address.html',data)
    return  JsonResponse({'result':result})




  