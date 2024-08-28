from itertools import count
from django.shortcuts import render 
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from .models import *
from basket.models import *
from django.core.paginator import Paginator


from django.db.models import Count,Max,Min,Sum,Case,When
from django.contrib import messages
# Create your views here.


def shop_list_view(request):
        get_product =   Product.objects.all().order_by('-created_at')
        
        print(n for n  in get_product)   
        
        pagi = Paginator(get_product,2)
        
        # GETTING PAGE NUMBER FROM URL
        page_num = request.GET.get('page')
        
        # GETTING PRODUCTS BY PAGE NUMBER
        products = pagi.get_page(page_num)
        product_pages_list = [n for n in pagi.page_range] 
    
        if request.method == 'GET':
            key  = request.POST.get('key')
            if  key == '001':
                products =   Product.objects.all().order_by('-created_at')
                content ={
                    'sale_products':get_product, 
                    'product_pages_list':product_pages_list,
                    'products': products,   
               
                 }

                result= render_to_string('store/shop.html',content)
                return  JsonResponse({'result':result})
                           
        else:
            products =   Product.objects.all().order_by('id')
            media   =    Media.objects.all()
       

        content = {
            'sale_products':get_product,   
            'products': products,
            'product_pages_list':product_pages_list,
            
        }
    
        return render(request,'store/shop.html',content)


def get_by_category_view(request,slug):
    products =   Product.objects.filter(category__slug=slug)
    featured_products = Product.objects.filter(is_featured=True)
    media   =    Media.objects.all()
    content = {
            'products':products,     
            'featured_products':featured_products,     
            'media':media,
            }
    return render(request,'store/shop.html',content)


def get_by_search_view(request):
    query = None
    if request.method == 'GET':
        query = request.GET.get("q")
        products =   Product.objects.filter(title__icontains=query,keywords__icontains=query,description__icontains=query)
        featured_products = Product.objects.filter(is_featured=True)
        media   =    Media.objects.all()
        content = {
                'query':query,
                'products':products,     
                'featured_products':featured_products,     
                'media':media,
                }
    return  render(request,'store/search.html',content)
          

def get_by_sort_view(request,slug):
    content = None
    if request.method == 'GET' and slug == 'New_listed' :
        products =   Product.objects.all().order_by('-created_at')
        media   =    Media.objects.all()
        featured_products = Product.objects.filter(is_featured=True)
       
    elif  slug == 'Lowest_price':
        products =   Product.objects.all().order_by('price')
        media   =    Media.objects.all()
        featured_products = Product.objects.filter(is_featured=True)
       
    elif  slug == 'Highest_price':
        products =   Product.objects.all().order_by('-price')
        media   =    Media.objects.all()
        featured_products = Product.objects.filter(is_featured=True)
       
    else :
        products =   Product.objects.all()
        media   =    Media.objects.all()
        featured_products = Product.objects.filter(is_featured=True)
       
    content = {
                'products':products,     
                'featured_products':featured_products,     
                'media':media,
            }
    return render(request,'store/sort.html',content)
    

def get_detail_view(request,slug,sku):

        variations  =  SubProduct.objects.filter(product__slug=slug,is_active=True)
        variant_img_gallery   =   Media.objects.filter(subproduct__product__slug=slug,subproduct=variations[0])   
        
        cl = Color.objects.filter(subproduct__product__slug=slug)
      
        colors =[]
        if request.user:
            print(request.GET.get('user'))
        for cl in cl:
            if cl not in colors:
                colors.append(cl)
        size = Size.objects.filter(subproduct__product__slug=slug,subproduct__color=list(colors)[0],subproduct__is_active=True)
        # wishlist
        if request.method == 'GET':
            if request.GET.get('passkey') == 'get_variant':
                # GETTING DATA FROM REQUEST
                variant_id  = request.GET.get('variant_id')
                color_id = request.GET.get('color_id')
                size_id = request.GET.get('size_id')
            
                variant  =  SubProduct.objects.filter(product__slug=slug,color=color_id)
           
                
                color = Color.objects.filter(subproduct__product__slug=slug).annotate(
                        relevancy=Count(Case(When(id=color_id, then=1)))
                        ).order_by('-relevancy')
                size = {v.size for v in variant}
                variant_img_gallery   =   Media.objects.filter(subproduct__in=variant)
                content = {
                'variation':variant,
                'variant_img_gallery':variant_img_gallery,
                'size':size,
                'color':color,
                }
                result= render_to_string('store/variation_detail.html',content)
                return  JsonResponse({'result':result})
       
        content = {
            'variation':variations,
            'variant_img_gallery':variant_img_gallery,
            'size':size,
            'colors':colors,
            }
        
        return render(request,'store/detail.html',content) 


   

