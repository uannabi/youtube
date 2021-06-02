from django.contrib import admin
from api.models import YoutubeChannel, YoutubeVideo

# Register your models here.
admin.site.register(YoutubeChannel)
admin.site.register(YoutubeVideo)
