# from rest_framework import serializers
# from .models import *


# from rest_framework import serializers
# from .models import CustomUser

# class CustomUserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=30)
#     email = serializers.EmailField()
#     password = serializers.CharField(min_length=8, write_only=True)
#     profile_img = serializers.ImageField(required=False)
#     bio = serializers.CharField(required=False)

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             profile_img=validated_data.get('profile_img'),
#             bio=validated_data.get('bio')
#         )
#         return user

#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'email', 'password', 'profile_img', 'bio')
