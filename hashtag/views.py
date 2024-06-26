import json
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F
from django.core.cache import cache

from .models import TagCount
from .serializers import TagCountSerializer
from .utils import filter_hashtags, remove_hashtag_prefix

# Create your views here.
class HashtagView(generics.ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        post = request.data.get('post', None)
        if post is None:
            return Response({'error': 'post is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        tags = remove_hashtag_prefix(filter_hashtags(post))
        for tag in tags:
            tag_obj = None
            try:
                tag_obj = TagCount.objects.get(tag=tag)
                tag_obj.count = F('count') + 1
                tag_obj.save()
            except TagCount.DoesNotExist:
                tag_obj = TagCount.objects.create(tag=tag)

        return Response({'success': 'tag count updated'}, status=status.HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        tag = kwargs.get('tag', None)
        if not tag:
            return Response({'error': 'tag is required'}, status=status.HTTP_400_BAD_REQUEST)

        tag_count = 0
        try:
            tag_count = TagCount.objects.get(tag=tag).count
        except TagCount.DoesNotExist:
            pass

        return Response({'message': 'success', 'count':tag_count}, status=status.HTTP_200_OK)

class HashtagSearchView(generics.ListAPIView):
    serializer_class = TagCountSerializer

    def get_queryset(self):
        tag = self.request.GET.get('tag', None)
        if tag:
            if tag[0] == '#':
                return TagCount.objects.filter(tag__icontains=tag[1:])
            return TagCount.objects.filter(tag__icontains=tag)
        return TagCount.objects.all()
    
    def get(self, request, *args, **kwargs):
        tag = self.request.GET.get('tag', None)
        tags = cache.get(tag)

        if tags:
            return Response(json.loads(tags), status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        cache.set(tag, json.dumps(serializer.data), 60)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        