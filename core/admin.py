from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .forms import *
# Register your models here.


# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm

#     list_display=['username','email','first_name','last_name','is_active']
#     list_filter=['username','email']
#     search_fields=['username','email']

#     fieldsets=[
#         (None,{'fields':['username','email']}),
#         ('Personal info',{'fields':['first_name','last_name','bio','profile_img']})
#     ]
#     add_fieldsets = [
#         (
#             None,
#             {
#                 "classes": ["wide"],
#                 "fields": ["username",'first_name','last_name','bio','profile_img','email', "password1", "password2"],
#             },
#         ),
#     ]
#     ordering=['username']



    

    

