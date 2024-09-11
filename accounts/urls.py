from django.urls import path
from .views import *
from django.contrib.auth import views as auth
from knox.views import LogoutView,LoginView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name ='logout'),
    path('users/',UserListView.as_view(),name='users'),
    path('users/<str:key>/',profile,name='profile'),
    path('email-confirmation/',confirm_email,name='confirm-email')
]