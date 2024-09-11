from django import forms
from .models import *
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
import json

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=CKEditorWidget(attrs={
        'cols':40
    }))
    class Meta:
        model=Comment
        fields=['comment']

class QuestionForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model=Question
        fields= ['title','description']
    
    

class QuestionEditForm(forms.ModelForm):
    title = forms.CharField(required=False)
    description = forms.CharField(widget=CKEditorWidget(),required=False)

    class Meta:
        model = Question
        fields = ['title', 'description']

