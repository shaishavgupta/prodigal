from rest_framework import serializers

from .models import TagCount

class TagCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagCount
        fields = '__all__'