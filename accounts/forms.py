from django import forms
from .models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm,TextInput,ChoiceField,Textarea

from django.contrib.auth.forms import UserChangeForm
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
                'class': "form-control", 
                'placeholder': 'Password'
                }))
    password2 = forms.CharField(
        label="Confirmation Password", widget=forms.PasswordInput(
            attrs={
                'class': "form-control", 
                'placeholder': 'Confirmation Password'
                }
        )
    )
    github_link = forms.URLField(
    max_length=255,
    required=False,
    label=False,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'GitHub Profile',
    })
)

    linkedin_link = forms.URLField(
        max_length=255,
        required=False,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'LinkedIn Profile',
        })
    )

    
    username=forms.CharField(label='Username',widget=TextInput(attrs={
                'class': "form-control", 
                'placeholder': 'Username'
                }))
    profile_img = forms.ImageField(required=False, widget=forms.FileInput)
    class Meta:
        
        model = CustomUser
        fields = ["username",'email','password1','password2','bio','profile_img','github_link','linkedin_link']
        widgets = {
            'email': TextInput(attrs={
                'class': "form-control", 
                'placeholder': 'Email'
                }),
            
            }

    def clean_username(self):
        username=self.cleaned_data.get("username")
        user_name=CustomUser.objects.filter(username=username)
        if user_name.exists():
            raise ValidationError('Username Taken.')
        else:
            return username
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2
    
    def clean_profile_img(self):
        profile_img = self.cleaned_data.get('profile_img')
        
        if profile_img:
            max_size = 10 * 1024 * 1024  
            
            if profile_img.size > max_size:
                raise forms.ValidationError('File size must be no more than 5 MB.')

        return profile_img

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserloginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'profile_img', 'bio', 'github_link', 'linkdin_link')

        widgets = {
            'email': TextInput(attrs={'class': "form-control", 'placeholder': 'Email'}),
            'username': TextInput(attrs={'class': "form-control", 'placeholder': 'Username'}),
        }
    
    profile_img = forms.ImageField(required=False, widget=forms.FileInput)

    def clean_profile_img(self):
        profile_img = self.cleaned_data.get('profile_img')
        
        if profile_img:
            max_size = 10 * 1024 * 1024  
            
            if profile_img.size > max_size:
                raise forms.ValidationError('File size must be no more than 5 MB.')

        return profile_img

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')

