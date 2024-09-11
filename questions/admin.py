from django.contrib import admin
from .models import *
from django.utils.html import mark_safe



@admin.action(description='تایید سوالات انتخاب شده')
def approve_questions(modeladmin,request,queryset):
    queryset.update(approve=True)


@admin.action(description='رد سوالات انتخاب شده')
def prohibit_questions(modeladmin,request,queryset):
    queryset.update(approve=False)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user','get_description','created_at', 'approve')
    search_fields = ['title']
    list_filter = ['tag', 'approve']
    actions = [approve_questions, prohibit_questions] 

    def get_description(self, obj):
        return mark_safe(obj.description)
    get_description.short_description = 'Description'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','created_at','question','is_answer']
    list_filter=['is_answer']

