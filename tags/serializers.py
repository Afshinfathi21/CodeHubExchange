from rest_framework import serializers
from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
