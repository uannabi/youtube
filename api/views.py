from django.shortcuts import render
from api.models import YoutubeVideo
# from myapp.serializers import PurchaseSerializer
from rest_framework import generics
# Create your views here.
from rest_framework import serializers
from taggit.models import Tag


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('id', 'name')
#
#
# class StringListField(serializers.ListField):
#     child = serializers.CharField()
#
#     def to_representation(self, data):
#         return ' '.join(data.values_list('name', flat=True))


class YoutubeVideoSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    @staticmethod
    def get_tags(obj):
        return ','.join(tag.name for tag in obj.tags.all())
    # tags = StringListField(required=False)

    class Meta:
        model = YoutubeVideo
        fields = (
            'title',
            'published_at',
            'tags',
            'view_count',
            'like_count',
            'dislike_count',
            'favorite_count',
            'comment_count'
        )


class YoutubeVideoList(generics.ListAPIView):
    serializer_class = YoutubeVideoSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = YoutubeVideo.objects.all()
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__name=tag)
        return queryset
