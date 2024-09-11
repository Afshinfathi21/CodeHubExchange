from django.contrib import admin
from .models import *


@admin.action(description='تایید موضوعات انتخاب شده')
def approve_questions(modeladmin,request,queryset):
    queryset.update(approve=True)


@admin.action(description='رد موضوعات انتخاب شده')
def prohibit_questions(modeladmin,request,queryset):
    queryset.update(approve=False)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['tagname','user','approve']
    list_filter=['user']
    actions = [approve_questions, prohibit_questions]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display=['name']