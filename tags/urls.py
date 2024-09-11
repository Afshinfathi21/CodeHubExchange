from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth
urlpatterns = [
    path('',tag_list,name='tags-list'),
    path('get-deps/',get_department_name,name='deps-name'),
    path('req-topic/',topic_request,name='req-topic'),
    path('get_tag_suggestions/', GetTagSuggestions.as_view(), name='get_tag_suggestions'),
]