from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from accounts.forms import *
from .models import *
from django.contrib.auth.models import Group

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display=['username','email','is_active']
    search_fields=['username','email']

    fieldsets=[
        (None,{'fields':['username','email']}),
        ('Personal info',{'fields':['bio','profile_img','is_active','is_staff']})
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username",'bio','profile_img','email', "password1", "password2",'is_active','is_staff'],
            },
        ),
    ]
    ordering=['username']

admin.site.unregister(Group)
admin.site.site_header='CodeHubExchange'