from django.shortcuts import render
from django .http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
import requests

def index(request):

    callapi=requests.get('http://127.0.0.1:8000/listings/r/view/')
    result=callapi.json()
    data=result['results']

    return render(request,'pages/index.html',{'data':data})

def about(request):

    #get realtor 
    realtors = Realtor.objects.order_by('-hire_date')

    #get MVP 
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }
    return render(request, 'pages/about.html', context)

def login(request):
    return render(request, 'account/login.html')

def register(request):
    return render(request,'account/register.html')

def single(request):
    return render(request,'pages/singleproperty.html')