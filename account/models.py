from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.shortcuts import get_object_or_404

# Create your models here.

class MyAccountManager(BaseUserManager):
    def  create_superuser(self,username,email,password, **other_fields):
            other_fields.setdefault('is_admin',True)
            other_fields.setdefault('is_staff',True)
            other_fields.setdefault('is_superadmin',True)
            other_fields.setdefault('is_superuser',True)
            other_fields.setdefault('is_active',True)
        
            if other_fields.get('is_staff') is not True:
                raise ValueError(
                        "superuser must be assigned to is_staff=True"
                )
        
            if other_fields.get('is_admin') is not True:
                raise ValueError(
                        "superuser must be assigned to is_admin=True"
                )
        
            if other_fields.get('is_superadmin') is not True:
                raise ValueError(
                        "superuser must be assigned to is_superadmin=True"
                )
                
            return self.create_user(username,email,password, **other_fields)

            # user = self.create_user(
            #     email = self.normalize_email(email),
            #     username = username,
            #     first_name = first_name,
            #     password=password,
            #     last_name= last_name
            # )
            # user.is_admin = True
            # user.is_staff = True
            # user.is_superadmin = True
            # user.is_active = True
            # user.save(using=self._db)
            # return user


    def  create_user(self, username,email,password=None,**other_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError(_('User must have an username'))

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

           
class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    optional_email= models.EmailField(max_length=100,unique=True,null=True,blank=True)
    phone = models.CharField(error_messages={'unique':"This phone has already been registered."},max_length=20,unique=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Acounts"

    def __str__(self):
       return  self.email

    def has_perm(self, perm , obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True



LABEL_CHOICES =(
    ('HM','Home'),
    ('OF','Office'),
)
ADDRESS_CHOICES =(
    ('BL','Billing'),
    ('SP','Shipping'),
)

class AddressBookManager(models.Manager):
    def create_addressbook(self,user,**data):
        # Create a new object
        
        inst ,created = self.get_or_create(profile=user,is_active=True,**data)
        if created:
            return inst
        return None
      
    
    def get_addressbook(self, **filters):
        # Retrieve objects based on filters
        return self.filter(**filters)
        # return get_object_or_404(self,**filters)
    
    def update_addressbook(self,user,obj,**data):
        # Update an existing object
        
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
        return obj 

                
    
    def delete_addressbook(self, obj):
        # Delete an object
        obj.delete()


    def create_default(self,user,obj,**data):
        inst = self.filter(profile=user)
        if inst.count() > 1:

            if (data['bill_default'] == True and obj.bill_default == False)  and (data['ship_default']  == True and obj.ship_default == False):
                
                inst.update(bill_default = False,ship_default = False)
                obj.bill_default = data['bill_default']
                obj.ship_default = data['ship_default']
            elif   (data['bill_default'] == True and obj.bill_default == False):

                inst.update(bill_default = False)
                obj.bill_default = data['bill_default']
                
            elif   (data['ship_default']  == True and obj.ship_default == False):

                inst.update(ship_default = False)
                obj.ship_default = data['ship_default']
        else:
            obj.bill_default = True
            obj.ship_default = True
        obj.save()
        return   obj

class AddressBook(models.Model):
    profile   = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,default='HM',choices=LABEL_CHOICES)
    first_name = models.CharField(default='',max_length=100)
    last_name = models.CharField(default='',max_length=100)
    phone = models.CharField(max_length=20,null=True,blank=True)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100,null=True,blank=True)
    country = CountryField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    ship_default = models.BooleanField(default=False)
    bill_default = models.BooleanField(default=False)
    postal_code = models.CharField(max_length=12,blank=True)
    address_type = models.CharField(max_length=200,default='SP',choices=ADDRESS_CHOICES)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    obj = AddressBookManager()
    objects = models.Manager()

    def __str__(self):
        return str(self.address_line_1)

