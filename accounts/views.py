from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
# from . models import Users
from . serializers import UserTokenObtainPairSerializer, UsersSerializer
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from email.message import EmailMessage
from django.template import Context
from django.template.loader import render_to_string
import smtplib
# # from .serializers import *
# from accounts.serializers import UsersSerializer
from django.shortcuts import render, redirect
from accounts import serializers
from accounts.models import Users
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import serializers



from accounts import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
  
  try:
    
    if 'first_name' not in request.data and request.data['type']  == 'customer':
      return Response({'status':'error', 'message': 'first_name required.'}, status=404)

    if 'first_name' not in request.data and request.data['type']  == 'seller':
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
        if 'first_name' in request.data and request.data['type']  == 'customer':

          first_name = request.data['first_name']  
          print('----------', first_name)

          emailSubject = "Welcome to Digital Press "
          print('+++++====', emailSubject)
            
          context = ({"name": first_name}) #Note I used a normal tuple instead of  Context({"username": "Gilbert"}) because Context is deprecated. When I used Context, I got an error > TypeError: context must be a dict rather than Context
          print('[[[[[[]]]]]', context)
            
            # html_content = render_to_string('welcome_email.html', context)
          html_content = render_to_string("welcome email testing", context)
          print('&&&&&&',html_content)

          try:
                #I used EmailMultiAlternatives because I wanted to send both text and html
              emailMessage = EmailMultiAlternatives(emailSubject, html_content, "Digital Press", [user])
              print('#####', EmailMessage)
              emailMessage.content_subtype = 'html'
              print(emailMessage)
              emailMessage.send(fail_silently=False)
              # send_mail(
              #         'Subject',
              #         '',
              #         'from@example.com',
              #         ['john@example.com', 'jane@example.com'],
              #     )
                
          except smtplib.SMTPException as e:
              print('There was an error sending an email: ', e) 
              print(e)
              error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
              print(error)
              raise serializers.ValidationError(error) 
 
    # return redirect('login')
    return Response({'status':'success', 'message': 'Successfully signed up please login.'}, status=201)
  
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
        
        if not (Users.objects.filter(email=request.data.get('email'), type='customer').count()==1):
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
        serializer = self.get_serializer(data=request.data)
        print("///////////////",serializer)

        serializer.is_valid(raise_exception=True)
        print(serializer)

        # try:
        #     serializer.is_valid(raise_exception=True)
        #     print("ssssssssssssssssssss",serializer.is_valid)
        #
        # except Exception as e:
        #
        #     return Response({'status': 'error', 'message': 'No activesss account found with the given credentials'}, status=403)
        #
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
        return Response(serializer.validated_data, status=200)

class SupplierLoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        if not (Users.objects.filter(email=request.data.get('email'), type='seller').count()==1):
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'status': 'error', 'message': 'No active account found with the given credentials'}, status=403)
            
        return Response(serializer.validated_data, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return Response({'status':'success','message': 'Logout Success'}, status=200)
  else:
    return Response({'status':'error','message': 'Method Not Allowed'}, status=405)




from celery.schedules import crontab
from django.http.response import HttpResponse
from django.shortcuts import render
# from .tasks import test_func
from accounts.tasks import send_mail_func
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("Sent")

# @receiver(emailsignal)
def schedule_mail(request,**kwargs):
    schedule, created = CrontabSchedule.objects.get_or_create(hour = 12, minute = 20)
    task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_"+"3", task='dashboard.tasks.send_mail_func')#, args = json.dumps([[2,3]]))
    return HttpResponse("Done")
