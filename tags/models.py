from django.db import models

from django.db.models import Count,OuterRef, Subquery
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime
class TagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            question_count=Count('question',filter=models.Q(question__approve=True)),
            todays_question_count=Count(
                'question',
                filter=models.Q(question__created_at__date=timezone.now().date(),question__approve=True)
            )
        )
    
class DepartmentManager(models.Manager):
    def with_question_counts(self):
        today = datetime.now().date()
        return self.annotate(
            total_questions=Count('tag__question', filter=models.Q(tag__question__approve=True,tag__approve=True), distinct=True),
            questions_asked_today=Count('tag__question', filter=models.Q(tag__question__created_at__date=today, tag__question__approve=True,tag__approve=True), distinct=True)
        )

class Department(models.Model):
    name = models.CharField(max_length=250)
    objects=DepartmentManager()
    def __str__(self):
        return self.name


from accounts.models import CustomUser
class Tag(models.Model):
    tagname=models.CharField( max_length=200)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=1)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    approve=models.BooleanField(default=False)
    objects=TagManager()
    def __str__(self) -> str:
        return self.tagname
    
    class Meta:
        verbose_name='Topic'


