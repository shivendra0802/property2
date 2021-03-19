from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from . models import Users
from . serializers import UserTokenObtainPairSerializer, UsersSerializer
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from email.message import EmailMessage
from django.template import Context
from django.template.loader import render_to_string
import smtplib
from .serializers import *
from django.shortcuts import render, redirect

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
  
  try:
    
    if 'first_name' not in request.data and request.data['type']  == 'front_user':
      return Response({'status':'error', 'message': 'first_name required.'}, status=404)
    if 'type' not in request.data:
      return Response({'status':'error', 'message': 'user type required.'}, status=404)


    
    password = request.data.get('password')

    serializer = UsersSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    data['is_active'] = True

    if not password:
        return Response({'status':'error','message': 'user password is required'}, status=404)

    if Users.objects.filter(email=data.get('email')).exists():
        return Response({'status':'error','message': 'Email is taken'}, status=400)
    else:
        user = Users(**data)
        user.set_password(password)
        user.save()
        # if 'first_name' in request.data and request.data['type']  == 'front_user':
        #   first_name = request.data['first_name']  

        #   emailSubject = "Welcome to Digital Press "
          
          
        #   context = ({"name": first_name}) #Note I used a normal tuple instead of  Context({"username": "Gilbert"}) because Context is deprecated. When I used Context, I got an error > TypeError: context must be a dict rather than Context

          
        #   html_content = render_to_string('welcome_email.html', context)

        #   try:
        #       #I used EmailMultiAlternatives because I wanted to send both text and html
        #       emailMessage = EmailMultiAlternatives(emailSubject, html_content, "Digital Press", [user])
        #       emailMessage.content_subtype = 'html'
        #       emailMessage.send(fail_silently=False)
              

        #   except smtplib.SMTPException as e:
        #       print('There was an error sending an email: ', e) 
        #       error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        #       raise serializers.ValidationError(error) 
 
    return redirect('login')
    # return Response({'status':'success', 'message': 'Successfully signed up please login.'}, status=201)
  
  except ValidationError as e: 
    return Response({'status':'error', 'message': e.detail}, status=404)
  except Exception as e: 
    return Response({'status':'error', 'message': str(e)}, status=404)


class UserProfileView(APIView):

  permission_classes = (IsAuthenticated,)

  def get(self, request, *args, **kwargs):

    return Response(UsersSerializer(request.user).data, status=200)

  def patch(self, request, *args, **kwargs):
    user = request.user

    serializer = UsersSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
    else:
      return Response(serializer.errors, status=400)

    return Response(serializer.data, status=201)


class FrontUserLoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        if not (Users.objects.filter(email=request.data.get('email'), type='front_user').count()==1):
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)

        except Exception as e:
            
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
            
        return Response(serializer.validated_data, status=200)

class AdminLoginTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request,*args, **kwargs):
        
        if not (Users.objects.filter(email=request.data.get('email'), type='admin').count()==1):
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
        serializer = self.get_serializer(data=request.data)
        
        #result=Users.objects.get(email=request.data['email'])
        
        
        try:
            serializer.is_valid(raise_exception=True)
            # uids=serializer.validated_data['id']
            # print("views", uid)
            
            
            
        except Exception as e:
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
        
        return redirect('dashbord')
        # return Response(serializer.validated_data, status=200)
# class SupplierLoginTokenObtainPairView(TokenObtainPairView):
#     serializer_class = UserTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs):
        
#         if not (Users.objects.filter(email=request.data.get('email'), type='supplier').count()==1):
#             return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
#         serializer = self.get_serializer(data=request.data)
        
#         try:
#             serializer.is_valid(raise_exception=True)
#         except Exception as e:
#             return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
            

#         return Response(serializer.validated_data, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return Response({'status':'success','message': 'Logout Success'}, status=200)
  else:
    return Response({'status':'error','message': 'Method Not Allowed'}, status=405)
