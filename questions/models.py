from django.db import models
from accounts.models import CustomUser
from tags.models import Tag
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Question(models.Model):
    title=models.CharField(max_length=200)
    description=RichTextField()
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag)
    views=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField( auto_now_add=True)
    approve=models.BooleanField(default=False)
    slug=models.SlugField(unique=True,allow_unicode=True,blank=True,max_length=300)

    def comment_count(self):
        try:
            return Comment.objects.filter(question=self).count()
        except Exception as e:
            return 0
        
    def answer_count(self):
        try:
            return Comment.objects.filter(question=self,is_answer=True).count()
        except Exception as e:
            return 0
    
    def get_tags(self):
        return [tag.tagname for tag in self.tag.all()]


    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    comment=RichTextField()
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    file=models.FileField(upload_to='comment/%Y%m%d/files',null=True,blank=True)
    is_answer=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f'{self.user} - {self.comment}'



