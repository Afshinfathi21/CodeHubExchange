from django.shortcuts import render,get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from django.http import JsonResponse
from questions.models import *
from discutions.models import *
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Q
from django.contrib.auth import logout
from django.contrib import messages
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from accounts.serializers import CustomUserChangeSerializer
from rest_framework.views import Response,status
from django.contrib.auth.decorators import login_required
from knox.models import AuthToken
from tags.models import Department
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['GET'])
def home(request):
    context={
        'departments':Department.objects.with_question_counts()
    }
    return render(request, 'home.html',context=context)


from django.views import View

class SearchView(View):

    def get(self, request, *args, **kwargs):
        search_key = request.GET.get('search_key', '')
        questions = Question.objects.filter(title__icontains=search_key,approve=True)
        users = CustomUser.objects.filter(username__icontains=search_key).exclude(username='admin')
        tags = Tag.objects.filter(tagname__icontains=search_key,approve=True)

        question_list = [{'type': 'question', 'text': question.title, 'slug': question.slug} for question in questions]
        user_list = [{'type': 'user', 'text': user.username} for user in users]
        tags_list = [{'type': 'tag', 'text': tag.tagname} for tag in tags]

        results = question_list + user_list + tags_list
        return JsonResponse(results, safe=False)


   
class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer=CustomUserChangeSerializer(instance=request.user)
        return render(request,'edit-profile.html',{'user':serializer.data})

    def post(self, request):
        serializer = CustomUserChangeSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request,'پروفایل با موفقیت اپدیت شد')
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

from datetime import datetime, timedelta
import pytz
from django.db.models import Count
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user=request.user
    acceptet_answer=Comment.objects.filter(user=user,is_answer=True).count()
    total_questions_waiting=Question.objects.filter(user=user,approve=False).count()
    answers=Question.objects.filter(comment__user=user).order_by('-created_at').distinct()
    current_user=CustomUser.objects.get(id=user.id)
    questions=Question.objects.all().filter(user=request.user).order_by('-created_at')
    views=questions.aggregate(total_views=Sum('views'))
    total_topics=Tag.objects.filter(user=user).count()
    total_topics_accepted=Tag.objects.filter(user=user,approve=True).count()



    tzinfo=pytz.timezone('Asia/Tehran')
    today = datetime.now(tz=tzinfo)
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = start_of_month.replace(month=start_of_month.month + 1) - timedelta(days=1)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6) 

    q = request.GET.get('questions')
    a = request.GET.get('answers')
    if q:
        if q == 'all':
            questions= questions.order_by('id')
        elif q == 'newest':
           questions= questions.order_by('-created_at')
        elif q == 'unaswered':
            questions= questions.annotate(answer_count=Count('comment'))
            questions= questions.filter(answer_count=0).order_by('id')
        elif q == 'month':
            questions= questions.filter(created_at__range=[start_of_month,end_of_month]).order_by('id')
        elif q == 'week':
            questions= questions.filter(created_at__range=[start_of_week,end_of_week]).order_by('id')
    if a:
        if a == 'all':
            answers= answers.order_by('id')
        elif a == 'newest':
           answers= answers.order_by('-created_at')
        elif a == 'month':
            answers= answers.filter(created_at__range=[start_of_month,end_of_month]).order_by('id')
        elif a == 'week':
            answers= answers.filter(created_at__range=[start_of_week,end_of_week]).order_by('id')
    context={
            'questions':questions,
            'user':current_user,
            'accepted_answers':acceptet_answer,
            'answers':answers,
            'total_views':views['total_views'],
            'waiting_questions':total_questions_waiting,
            'total_topics':total_topics,
            'accepted_topics':total_topics_accepted,
        }
    return render(request,'dashboard.html',context=context)

from knox.views import LogoutAllView  
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile(request,username):
    user=CustomUser.objects.get(username=username)
    user.delete()
    LogoutAllView.post(self=LogoutAllView,request=request)
    messages.success(request,"اکانت شما با موفقیت حذف شد")
    return Response("Account has been deleted",status=status.HTTP_202_ACCEPTED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_answer(request):
        try:
            checked_answer_ids = request.POST.getlist('answers[]')
            unchecked_answer_ids = request.POST.getlist('unchecked_answers[]')
            Comment.objects.filter(id__in=checked_answer_ids).update(is_answer=True)
            Comment.objects.filter(id__in=unchecked_answer_ids).update(is_answer=False)
            messages.success(request,'با موفقیت ثبت شد')
            return Response('Updated SuccessFully',status=status.HTTP_202_ACCEPTED)
        except:
             return Response('failed to update.',status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def question_delete(request,pk):
        question=Question.objects.get(id=pk)
        question.delete()
        messages.success(request,"سوال با موفقیت حذف شد")
        return Response('SuccessFully Deleted.',status=status.HTTP_202_ACCEPTED)
     

def custom_bad_request(request, exception):
    return render(request, '400.html', status=400)

def custom_permission_denied(request, exception):
    return render(request, '403.html', status=403)

def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)

def custom_server_error(request):
    return render(request, '500.html', status=500)

