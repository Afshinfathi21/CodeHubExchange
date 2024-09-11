from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from questions.models import Question

@receiver(pre_save, sender=Question)
def create_question_slug(sender, instance, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title,allow_unicode=True)
        unique_slug = slug
        counter = 1
        while Question.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        instance.slug = unique_slug