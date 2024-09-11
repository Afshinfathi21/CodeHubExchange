from django.urls import path,re_path
from .views import *


urlpatterns = [
    path('department/<str:department>',questions,name='department-questions'),
    path('topic/<str:tag>',questions,name='tag-questions'),
    path('',questions,name='total-questions'),
    path('question/<str:slug>/', QuestionDetailAPIView.as_view(), name='question-detail'),
    path('ask/',Askquestion.as_view(),name='ask'),
    re_path(r'question/(?P<slug>[-\w]+)/edit', EditQuestion.as_view(), name="edit-question"),

]