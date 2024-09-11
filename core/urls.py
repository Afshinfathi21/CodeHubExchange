from django.urls import path,include,re_path
from .views import *
from django.contrib.auth import views as auth
from django.contrib import admin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('questions/',include('questions.urls')),
    # path('api/discutions',include('discutions.urls')),
    path('topics/',include('tags.urls')),


    
    path('',home,name='home'),
    path('dashboard/',dashboard,name='dashboard'),
    path('edit-profile/',EditProfileView.as_view(),name='edit-profile'),
    path('dashboard/question/update-answer',update_answer,name='update-answers'),
    path("dashboard/question/delete/<str:pk>", question_delete, name="delete-question"),
    path('<str:username>/delete-profile/',delete_profile,name='delete-profile'),

    path('search/',SearchView.as_view(),name='search'),
]


