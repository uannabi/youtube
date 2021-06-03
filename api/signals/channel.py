from django.db.models.signals import post_save, post_delete
from api.models import YoutubeChannel
from django.dispatch import receiver


@receiver(post_save, sender=YoutubeChannel)
@receiver(post_delete, sender=YoutubeChannel)
def update_performance(sender, instance, created=None, *args, **kwargs):
    for video in instance.youtube_videos.all():
        video.save()
