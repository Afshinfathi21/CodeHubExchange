from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model,logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage,send_mail
from django.http import JsonResponse
from django.utils import timezone

from knox.models import AuthToken
from knox.views import LoginView

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView,Response
from rest_framework.decorators import api_view
from .models import *
from .tokens import *
from .serializers import *
import requests

from django.urls import reverse


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(
            request, f'Problem sending email to {to_email}, check if you typed it correctly.')
class RegisterAPIView(APIView):
    def post(self, request):
        
        if not request.user.is_authenticated:
            next_url= reverse("confirm-email")
            serializer = UserCreationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.is_active = False
                user.save()
                # activateEmail(request, user, serializer.validated_data.get('email'))
                
                return JsonResponse(
                    {
                        'next_url':next_url, 
                    }
                )
            else:
                return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You are already authenticated."}, status=status.HTTP_403_FORBIDDEN)
    

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(
            request=request,
            template_name="register.html",
        )

class LoginAPIView(LoginView):
    permission_classes=[permissions.AllowAny]
    def get_token_limit_per_user(self):
        return super().get_token_limit_per_user()
    def get_token_ttl(self):
        return super().get_token_ttl()
    
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            next_url = request.GET.get('next', '/')
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user=serializer.validated_data
                token_limit_per_user = self.get_token_limit_per_user()
                if token_limit_per_user is not None:
                    now = timezone.now()
                    token = user.auth_token_set.filter(expiry__gt=now)
                    if token.count() >= token_limit_per_user:
                        return Response(
                            status=status.HTTP_403_FORBIDDEN
                        )
                messages.success(
                            request, f"عزیز خوش امدی <b>{user.username}</b>")
                token_ttl = self.get_token_ttl()
                instance, token = AuthToken.objects.create(user, token_ttl)
                if user and isinstance(user, CustomUser) and user.is_superuser:
                    login(request,user)
                response= JsonResponse(
                    {
                        'next_url':next_url,
                        
                    }
                )
                response.set_cookie(key='LOGGED_IN',value=token,httponly=True,expires=instance.expiry)
                return response
            else:
                return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
        return redirect('login')
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'login.html')
    
from knox.views import LogoutView

class Logout(LogoutView):
    def post(self, request, format=None):
        if request.user.is_superuser or request.user.is_staff and request.user.is_authenticated:
            logout(request)
        response=super().post(request, format)
        response.delete_cookie('LOGGED_IN')
        return response
    

from rest_framework.pagination import PageNumberPagination

class CustomUserPagination(PageNumberPagination):
    page_size = 16
class UserListView(APIView):
    pagination_class = CustomUserPagination
    template_name = 'users.html'

    def get(self, request, format=None):
        users = CustomUser.objects.filter(is_superuser=False, is_active=True).order_by('pk')
        paginator = CustomUserPagination()
        result_page = paginator.paginate_queryset(users, request)

        return render(request, self.template_name, {
            'object_list': result_page,
            'page_obj': paginator.page
        })


from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from questions.models import Comment

@api_view(['GET'])
def profile(request, key):

    User = get_user_model()
    user = get_object_or_404(User, username=key)
    answer_count=Comment.objects.filter(user=user,is_answer=True).count()
    context={
        'user_profile': user,
        'answer_count':answer_count,
    }
    return render(request, 'user-profile.html', context=context)

@api_view(['GET'])
def confirm_email(request):
    return render(request,'waiting_for_confirmation.html')