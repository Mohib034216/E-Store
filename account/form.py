from django.contrib.auth.forms import (AuthenticationForm)
from .models import Account, AddressBook
from django import forms
from django_countries.fields import CountryField
from django.shortcuts import get_object_or_404
from django.db.models import Q

# from django_countries.widgets import CountrySelectWidget


LABEL_CHOICES =(
    ('HM','Home'),
    ('OF','Office'),
)
  

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    

class CustomUserForm(forms.ModelForm):
    username  = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Username'}))
    email     = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Enter Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Confirm Password'}))
    
    class Meta:
        model = Account
        fields= ['username','email','password1','password2']

    def clean_username(self):
        user_name = self.cleaned_data['username'].lower()
        r= Account.objects.filter(username=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Passwords do not match.")
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, that is already exists")
        return email

class AddressUserForm(forms.Form):
    # id =forms.CharField(widget = forms.TextInput(attrs={
    #             'class':'form-control',
    #             'id':'addressform-id','placeholder':"ID",'hidden':'True'}))
    first_name=forms.CharField(widget = forms.TextInput(attrs={
                'class':'form-control',
                'id':'addressform-firstName','placeholder':"First Name"}))
    last_name= forms.CharField(widget = forms.TextInput(attrs={
                'class':'form-control',
                'id':'addressform-lastName','placeholder':"Last Name"}))
    phone= forms.CharField(widget = forms.TextInput(attrs={
                'class':'form-control',
                'id':'addressform-phone','placeholder':"+92XXXXXXXX",}))
            
    country= CountryField(blank_label="(select country)").formfield()
    address_line_1 = forms.CharField(widget = forms.Textarea(attrs={
                'class':'form-control',
                'id':'addressform-address',
                'placeholder':"1234 Main St",'style':'resize:none;' ,}))
    address_line_2 = forms.CharField(required=False,widget = forms.TextInput(attrs={"cols": 80, "rows": 20,
                'class':'form-control',
                'id':'addressform-optional_address',
                'placeholder':"Apartment or suite", }))
    
    title = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class':'og-form-addresstag-check','id':'addressform-label_tags',}),
        choices=LABEL_CHOICES, 
    )
    ship_default = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id':'addressform-ship-default','class':'form-check-input'}))
    bill_default = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id':'addressform-bill-default','class':'form-check-input'}))
    
   

    def address_fields_clean(options):
        data = {}
        for x,y in options.cleaned_data.items():
            if  x != 'ship_default' and x != 'bill_default' :
              data.update({x:y})
        return data

    def default_fields_clean(options):
        data = {}
        for x,y in options.cleaned_data.items():
            if  x == 'ship_default' or x == 'bill_default' :
              data.update({x:y})
        return data




    # def fields_clean(options):
    #     data = {}
    #     for x,y in options.cleaned_data.items():
    #         data.update({x:y})
    #     return data
    



    def get_form_data(pk):
        instance = get_object_or_404(AddressBook,pk=pk)
        user_data = {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'country': instance.country.code,
            'phone': instance.phone,
            'address_line_1': instance.address_line_1,
            'address_line_2': instance.address_line_2,
            'title': instance.title,
            'ship_default': instance.ship_default,
            'bill_default': instance.bill_default,}
        return user_data




class BillingCustomUserForm(forms.Form):  

            first_name=forms.CharField(widget = forms.TextInput(attrs={
                'class':'form-control',
                'id':'firstName','placeholder':"First Name"}))
            last_name= forms.CharField(widget = forms.TextInput(attrs={
                'class':'form-control',
                'id':'lastName','placeholder':"Last Name    "}))
            
            optional_email= forms.EmailField(required=False,widget = forms.TextInput(attrs={
                'class':'form-control',
                'id':'firstName','placeholder':"user@example.com",}))
            phone= forms.CharField(widget = forms.TextInput(attrs={
                'class':'form-control',
                'id':'firstName','placeholder':"+92XXXXXXXX",}))
            
            country= CountryField(blank_label="(select country)").formfield()
            address= forms.CharField(widget = forms.Textarea(attrs={
                'class':'form-control',
                'id':'firstName',
                'placeholder':"1234 Main St",'style':'resize:none;' ,}))
            optional_address= forms.CharField(required=False,widget = forms.TextInput(attrs={"cols": 80, "rows": 20,
                'class':'form-control',
                'id':'firstName',
                'placeholder':"Apartment or suite", }))
            postal_code=forms.CharField(widget = forms.TextInput(attrs={
                'class':'form-control',
                'id':'firstName','placeholder':"54863",}))

class ShippingCustomUserForm(forms.Form):  
            # ship_first_name=forms.CharField(widget = forms.TextInput(attrs={
            #     'class':'form-control',
            #     'id':'firstName','placeholder':"First Name"}))
            # ship_last_name= forms.CharField(widget = forms.TextInput(attrs={
            #     'class':'form-control',
            #     'id':'lastName','placeholder':"Last Name    "}))
            
            ship_country= CountryField(blank_label="(select country)").formfield()
            ship_address= forms.CharField(widget = forms.Textarea(attrs={
                'class':'form-control',
                'id':'firstName',
                'placeholder':"1234 Main St",'style':'resize:none;' ,}))
            ship_optional_address= forms.CharField(required=False,widget = forms.TextInput(attrs={"cols": 80, "rows": 20,
                'class':'form-control',
                'id':'firstName',
                'placeholder':"Apartment or suite", }))
            ship_postal_code=forms.CharField(widget = forms.TextInput(attrs={
                'class':'form-control',
                'id':'firstName','placeholder':"54863",}))
