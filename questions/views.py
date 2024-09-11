from rest_framework.views import APIView

from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .serializers import QuestionSerializer, CommentSerializer

from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.contrib import messages
from knox.auth import TokenAuthentication
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.db.models import Count
from rest_framework.views import Response,status

class QuestionDetailAPIView(APIView):

    def get(self, request, slug):
        user=request.user.id
        question = get_object_or_404(Question, slug=slug)

        viewed_questions = request.session.get('viewed_questions', [])

        if question.pk not in viewed_questions:
            question.views += 1
            question.save()

            viewed_questions.append(question.pk)
            request.session['viewed_questions'] = viewed_questions

        related_questions = Question.objects.filter(
            tag__in=question.tag.all()).exclude(id=question.id).distinct()[:4]
        comments = Comment.objects.all().filter(question=question)
        context = {
            'question': QuestionSerializer(question).data,
            'comments': CommentSerializer(comments, many=True).data,
            'related_questions': QuestionSerializer(related_questions, many=True).data,
            'form': CommentForm(),
            'qe_form': QuestionEditForm(initial={'title': question.title, 'description': question.description}),
            'req_user':user
        }
        return render(request, 'question-detail.html', context)

    @method_decorator(login_required(login_url='login'))
    @permission_classes([IsAuthenticated])
    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        form=CommentForm(request.POST,request.FILES)
        user=request.user
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user=user
            new_comment.question_id=question.pk
            new_comment.save()
            messages.success(request, f'ممنون از پاسخ شما.پاسخ شما ثبت شد ')
            return redirect(reverse('question-detail', args=[str(question.slug)]))
        else:
            messages.error(request, f'مشکلی پیش امده لطفا اطلاعات را چک کنید')
            return redirect(reverse('question-detail', args=[str(question.slug)]))
    

from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned

class Askquestion(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        form = QuestionForm()
        return render(request, 'ask-question.html', {'form': form})

    def post(self, request):
        user = request.user
        post_data = request.POST.copy()
        raw_tag_names = post_data.getlist('tag')
        tag_names = []

        for raw_tag in raw_tag_names:
            tag_names.extend(raw_tag.split(','))

        tag_names = [tag.strip() for tag in tag_names if tag.strip()]

        
        form = QuestionForm(post_data)
        invalid_tag_names = []
        for tag_name in tag_names:
            try:
                tag = Tag.objects.get(tagname=tag_name, approve=True)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                invalid_tag_names.append(tag_name)
        
        if invalid_tag_names:
            invalid_tags_str = ', '.join(invalid_tag_names)
            message = {
            'content': f"خطا در ایجاد سوال. تگ‌های نامعتبر: {invalid_tags_str}",
            'tags': 'danger',
            'success':False
            }
            return JsonResponse({'message':message})

        if form.is_valid():
            new_qs = form.save(commit=False)
            new_qs.user = user
            tags = Tag.objects.filter(tagname__in=tag_names, approve=True)
            
            new_qs.save()
            new_qs.tag.set(tags)
            messages.success(request, f'.سوال با موفقیت ثبت شد لطفا منتظر تایید از سمت ادمین بمانید')
            message = {
            'success':True
            }
            return JsonResponse({'message':message})
        else:
            message = {
            'content':  "خطا در ایجاد سوال.لطفا اطلاعات داده شده را چک کنید",
            'tags': 'danger',
            'success':False
            }
            return JsonResponse({'message':message})

from datetime import datetime, timedelta
import pytz
@api_view(["GET"])
def questions(request,tag=None,department=None):
    tzinfo=pytz.timezone('Asia/Tehran')
    today = datetime.now(tz=tzinfo)
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = start_of_month.replace(month=start_of_month.month + 1) - timedelta(days=1)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6) 

    all_questions = Question.objects.all().filter(approve=True,tag__approve=True).order_by('id').distinct()

    if tag:
        all_questions= all_questions.filter(tag__tagname=tag).distinct()
    
    elif department:
       all_questions= all_questions.filter(tag__department__name=department).distinct()

    tab = request.GET.get('tab')
    if tab:
        if tab == 'all':
            all_questions= all_questions.order_by('id')
        elif tab == 'newest':
           all_questions= all_questions.order_by('-created_at')
        elif tab == 'unaswered':
            all_questions= all_questions.annotate(answer_count=Count('comment'))
            all_questions= all_questions.filter(answer_count=0).order_by('id')
        elif tab == 'month':
            all_questions= all_questions.filter(created_at__range=[start_of_month,end_of_month]).order_by('id')
        elif tab == 'week':
            all_questions= all_questions.filter(created_at__range=[start_of_week,end_of_week]).order_by('id')

    paginator = Paginator(all_questions, 8)

    page = request.GET.get('page')

    try:
        questions_page = paginator.page(page)
    except PageNotAnInteger:
        questions_page = paginator.page(1)
    except EmptyPage:
        questions_page = paginator.page(paginator.num_pages)

    return render(request, 'questions.html', {'questions_page': questions_page,'questions':all_questions})

class EditQuestion(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        red=request.META.get('HTTP_REFERER', '/')
        print(red)
        form = QuestionEditForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request,'تغیر سوال با موفقیت انجام شد')
            return redirect(red)
        else:
            messages.error(request, "خطا در انجام تغیر")
            return redirect(red)
