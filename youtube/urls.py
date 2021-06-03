"""youtube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.fetch_youtube_data import get_channel_videos
from api.views import YoutubeVideoList
from rest_framework.response import Response
from rest_framework.views import APIView


class RootView(APIView):
    """
    RESTFul Documentation of my app
    """

    def get(self, request, *args, **kwargs):
        api_root = {'fetch data': request.build_absolute_uri('channel/'),
                    'filter videos': request.build_absolute_uri('videos'),

                    }
        return Response(api_root)


urlpatterns = [
    path('', RootView.as_view()),
    path('admin/', admin.site.urls),
    path('channel/<str:channel_id>', get_channel_videos),
    path('videos', YoutubeVideoList.as_view())
]
