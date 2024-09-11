from django.db import models
from accounts.models import *
from questions.models import *
# Create your models here.


class SubTopic(models.Model):
    name=models.CharField(max_length=250)

class Topic(models.Model):
    name=models.CharField(max_length=250)
    sub=models.ForeignKey(SubTopic,on_delete=models.CASCADE)

class Discution(models.Model):
    title=models.CharField(max_length=300)
    description=models.TextField()
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    views=models.PositiveIntegerField(default=0)
    topic=models.ForeignKey(SubTopic, on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField( auto_now_add=True)
        
    def __str__(self):
        return self.title