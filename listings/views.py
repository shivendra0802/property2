from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.serializers import Serializer
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from rest_framework import viewsets
from .serializers import *
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from django.http import JsonResponse

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)



def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        print(keywords)
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    #city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    #Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    #Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__iexact=price)

    context = {
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'listings': queryset_list
    }
    return render(request, 'listings/search.html', context)

class ListingView(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
    # return redirect('displaydata')

def displaydata(request):
    callapi=requests.get('http://127.0.0.1:8000/listings/r/view/')
    result=callapi.json()
    # data=result['results']
    # return render(request,'pages/index.html',{'data':data})
    return render(request, 'pages/index.html')

    



class ManageListingView(APIView):
    def get(self, request, format=None):
        pass
        # Serializer = ListingSerializer.
        # return Response(
        #         {'error': 'Something went wrong when creating listing'},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )
    def post(self, request, format=None):
        try:
            user = request.user

            # if not user.is_realtor:
            #     return Response(
            #         {'error': 'User doest not have necessary data to create this listing data'},
            #         status=status.HTTP_403_FORBIDDEN
            #     )

            data = request.data

            title           = data['title']
            slug            = data['slug']
            address         = data['address']    
            city            = data['city']
            state           = data['state']
            zipcode         = data['zipcode']
            description     = data['description']
            price           = data['price']
            
            if Listing.objects.filter(slug=slug).is_exists():
                return Response (
                    {'error': 'Listing with this objects is already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try: 
                price = int(price)
            except:
                return Response(
                    {'error': 'Price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )    

            # try: 
            #     price = float(price)
            # except:
            #     return Response(
            #         {'error': 'Price must be an integer'},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )    
                
            bedrooms = data['bedrooms']

            try: 
                bedroom = int(bedrooms)
            except:
                return Response(
                    {'error': 'Bedroom must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )    

            gaurage = data['gaurage']

            try:
                gaurage = int(gaurage)
            except:
                return Response(
                    {'error': 'Gaurage must be an integer'}
                )        
            photo_main   = data['photo_main']
            photo_1      = data['photo_1']
            photo_2      = data['photo_2']
            photo_3      = data['photo_3']
            photo_4      = data['photo_4']
            photo_5      = data['photo_5']
            is_published = data['is_published']

            if is_published == 'True':
                is_published = True
            else:
                is_published = False    

            Listing.objects.create(
                realtor = user.email,
                title   = title,
                address = address,
                slug    = slug,
                city    = city,
                state   = state,
                zipcode = zipcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                photo_main=photo_main,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                photo_4=photo_4,
                is_published=is_published
            )    

            return Response({
                'success': 'Listing created successfully'},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {'error': 'Something went wrong when creating listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({'status': status.HTTP_201_CREATED})         
