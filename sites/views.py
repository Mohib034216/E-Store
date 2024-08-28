from django.shortcuts import render
from django.shortcuts import HttpResponse
from store.models import *
from django.template.loader import render_to_string
from django.conf import settings
# Create your views here.


    

def home(request):

        featured_products =  Product.objects.filter(is_featured=True)[:20]
        latest_products  =  Product.objects.filter(is_featured=True).order_by('-created_at')[:6]
        context = {
                'email':settings.EMAIL_HOST_USER,
                'user':request.user,
                'featured_products':featured_products,
                'latest_products':latest_products, 
                }
        return render(request,'index.html',context)


