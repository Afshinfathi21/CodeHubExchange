from rest_framework import serializers
from .models import Question, Comment

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'comment','is_answer' ,'user', 'question', 'file', 'created_at']

    def get_user(self, obj):
        user_data = {
            'id': obj.user.id,
            'username': obj.user.username,
            'profile_img_url': obj.user.profile_img.url
        }
        return user_data

class QuestionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%H:%M %d-%m-%Y')
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'user', 'tag', 'views', 'created_at', 'comments','slug']

    def create(self, validated_data):
        comments_data = validated_data.pop('comments', [])
        question = Question.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(question=question, **comment_data)
        return question
    
    def get_user(self, obj):
        user_data = {
            'id': obj.user.id,
            'username': obj.user.username,
            'profile_img_url': obj.user.profile_img.url
        }
        return user_data
