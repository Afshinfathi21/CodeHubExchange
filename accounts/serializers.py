from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_img']

    def get_profile_img(self, user):
        
        if user.profile_img:
            return user.profile_img.url 
        return None



class UserCreationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True,min_length=8)
    password2 = serializers.CharField(write_only=True)
    github_link = serializers.URLField(max_length=255, required=False, allow_blank=True)
    linkedin_link = serializers.URLField(max_length=255, required=False, allow_blank=True)
    profile_img = serializers.ImageField(required=False, max_length=None, use_url=True)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['username'].error_messages['required']='نام کاربری نمیتواند خالی باشد'
        self.fields['username'].error_messages['blank']='نام کاربری نمیتواند خالی باشد'
        self.fields['email'].error_messages['required']='ایمیل نمیتواند خالی باشد'
        self.fields['email'].error_messages['blank']='ایمیل نمیتواند خالی باشد'
        self.fields['bio'].error_messages['required']='درباره خودت نمیتواند خالی باشد'
        self.fields['bio'].error_messages['blank']='درباره خودت نمیتواند خالی باشد'
        self.fields['password1'].error_messages['required']='رمز عبور نمیتواند خالی باشد'
        self.fields['password1'].error_messages['blank']='رمز عبور نمیتواند خالی باشد'
        self.fields['password2'].error_messages['required']='رمز عبور نمیتواند خالی باشد'
        self.fields['password2'].error_messages['blank']='رمز عبور نمیتواند خالی باشد'
    
    class Meta:
        model = CustomUser
        fields = ["username", 'email', 'password1', 'password2', 'bio', 'profile_img', 'github_link', 'linkedin_link']

    def validate_username(self, value):
        user_name = CustomUser.objects.filter(username=value)
        if user_name.exists():
            raise serializers.ValidationError('نام کاربری قبلا استفاده شده')
        return value

    def validate_password2(self, value):
        password1 = self.initial_data.get("password1")
        password2 = value
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError("رمز عبور با تکرار رمز متفاوت است")
        return value

    def validate_profile_img(self, value):
        if value:
            max_size = 2 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError('حجم عکس پروفایل کمتر از 2 مگابایت باشه')
        return value

    def create(self, validated_data):
        validated_data.pop('password1', None)
        password2 = validated_data.pop('password2', None)
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password2)
        user.save()

        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        print(data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('اطلاعات غلط')



class CustomUserChangeSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(required=False)
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['username'].error_messages['required']='نام کاربری نمیتواند خالی باشد'
        self.fields['username'].error_messages['blank']='نام کاربری نمیتواند خالی باشد'
        self.fields['email'].error_messages['required']='ایمیل نمیتواند خالی باشد'
        self.fields['email'].error_messages['blank']='ایمیل نمیتواند خالی باشد'
        self.fields['bio'].error_messages['required']='درباره خودت نمیتواند خالی باشد'
        self.fields['bio'].error_messages['blank']='درباره خودت نمیتواند خالی باشد'
    

    class Meta:
        model = CustomUser
        fields = ('username','email' ,'profile_img', 'bio', 'github_link', 'linkdin_link')


    def validate_profile_img(self, value):
        if value:
            max_size = 2 * 1024 * 1024

            if value.size > max_size:
                raise serializers.ValidationError('حجم عکس پروفایل کمتر از 2 مگابایت باشه')

        return value
