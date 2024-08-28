from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
# Create your views here.


def testedhome_view(request):
    return HttpResponse('home')

def tested_view(request,sku):
    return HttpResponse(sku)