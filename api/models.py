from django.db import models
from taggit.managers import TaggableManager
import statistics


# Create your models here.

class YoutubeChannel(models.Model):
    channel_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    view_count = models.IntegerField()
    subscriber_count = models.IntegerField()
    video_count = models.IntegerField()
    published_at = models.DateTimeField()
    view_median = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        self.view_median = self.get_view_median()
        super(YoutubeChannel, self).save(*args, **kwargs)

    def get_view_median(self):
        increased_view_list = list(self.youtube_videos.values_list('increased_view_count', flat=True))
        return statistics.median(increased_view_list)

    def __str__(self):
        return self.title


class YoutubeVideo(models.Model):
    channel = models.ForeignKey(YoutubeChannel, on_delete=models.CASCADE, related_name='youtube_videos')
    video_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    published_at = models.DateTimeField()
    tags = TaggableManager(blank=True)
    previous_view_count = models.IntegerField(null=True, blank=True)
    view_count = models.IntegerField()
    increased_view_count = models.IntegerField(null=True, blank=True)
    performance = models.FloatField(null=True, blank=True)
    like_count = models.IntegerField()
    dislike_count = models.IntegerField()
    favorite_count = models.IntegerField()
    comment_count = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        self.performance = self.get_performance()

        super(YoutubeVideo, self).save(*args, **kwargs)

    def get_performance(self):
        if self.channel.view_median<1:
            return self.increased_view_count/1
        return self.increased_view_count / self.channel.view_median

    def __str__(self):
        return self.title
