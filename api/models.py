from django.db import models
from taggit.managers import TaggableManager


# Create your models here.

class YoutubeChannel(models.Model):
    channel_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    view_count = models.IntegerField()
    subscriber_count = models.IntegerField()
    video_count = models.IntegerField()
    published_at = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class YoutubeVideo(models.Model):
    channel = models.ForeignKey(YoutubeChannel, on_delete=models.CASCADE, related_name='youtube_videos')
    video_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    published_at = models.DateTimeField()
    tags = TaggableManager(blank=True)
    view_count = models.IntegerField()
    like_count = models.IntegerField()
    dislike_count = models.IntegerField()
    favorite_count = models.IntegerField()
    comment_count = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
