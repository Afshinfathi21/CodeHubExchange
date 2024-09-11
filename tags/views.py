from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.db import IntegrityError
from .models import *
from tags.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import Response,status
from django.contrib import messages
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def tag_list(request):
    tags=Tag.objects.filter(approve=True)
    paginator = Paginator(tags, 16)

    page = request.GET.get('page')

    try:
        tags_page = paginator.page(page)
    except PageNotAnInteger:
        tags_page = paginator.page(1)
    except EmptyPage:
        tags_page = paginator.page(paginator.num_pages)
    return render(request,'tags.html',{'tags':tags,'tags_page':tags_page})


@api_view(['GET'])
def get_department_name(request):
    objects = Department.objects.all()
    names = [obj.name for obj in objects]
    return Response(names)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def topic_request(request):
    if request.method == 'POST':
        tagname = request.data.get('tagname')
        selected_department = request.data.get('selectedDepartment')
        dep=Department.objects.get(name=selected_department)
        username=request.data.get('user')
        user=CustomUser.objects.get(username=username)
        try:
            Tag.objects.create(tagname=tagname, department=dep,user=user, approve=False)
            messages.success(request, 'درخواست شما با موفقیت ثبت شد')
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            messages.error(request, 'درخواست شما ثبت نشد لطفا مجددا تلاش کنید')
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
from django.http import JsonResponse
from django.views import View

from django.http import JsonResponse
from django.views import View
from .models import Tag

class GetTagSuggestions(View):
    def get(self, request):
        tag_objects = Tag.objects.filter(approve=True)
        tags_data = [tag.tagname for tag in tag_objects]
        return JsonResponse({'tags': tags_data})

