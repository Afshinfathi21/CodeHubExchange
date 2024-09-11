from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class CustomURLValidator(URLValidator):
    message = 'لینک وارد شده معتبر نیست.'  # Default message for invalid URL

    def __init__(self, message=None, code=None):
        super().__init__()
        if message:
            self.message = message
        if code:
            self.code = code

    def __call__(self, value):
        try:
            super().__call__(value)
        except ValidationError:
            raise ValidationError(self.message, code=self.code)

def user_directory_path(instance, filename):
   return 'users/%s/%s' % (instance.username, filename)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, error_messages={
        'unique': "این نام کاربری قبلاً استفاده شده است."
    })
    email = models.EmailField(unique=True, 
        error_messages={
            'unique': "این ایمیل قبلاً ثبت شده است.",
        }
        )
    profile_img = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    bio = models.CharField(max_length=255)
    github_link = models.URLField(max_length=250, blank=True, null=True)
    linkdin_link = models.URLField(max_length=250, blank=True, null=True)

