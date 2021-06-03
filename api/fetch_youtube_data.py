from googleapiclient.discovery import build
from api.models import YoutubeChannel, YoutubeVideo
from django.http import HttpResponse

api_key = "AIzaSyAwqoA4BmlRaXWPU-v4ZqsOOB3kICxu8aE"
youtube = build('youtube', 'v3', developerKey=api_key)


# channel_id = 'UCcRkS0t0Ss-RQ3wJd6n_2Mg'


def get_videos_stats(video_ids, channel_id):
    # print(video_ids)
    # stats = []
    # for i in range(0, len(video_ids), 50):
    #     res = youtube.videos().list(id=','.join(video_ids[i:i + 50]),
    #                                 part='snippet').execute()
    #     stats += res['items']

    # return stats
    channel_object = YoutubeChannel.objects.filter(channel_id=channel_id).first()
    # print(channel_object)
    for video_id in video_ids:
        res = youtube.videos().list(id=video_id, part='snippet,statistics').execute()
        # channel = YoutubeChannel.objects.get

        title = res['items'][0]['snippet']['title']
        published_at = res['items'][0]['snippet']['publishedAt']
        try:
            tags = res['items'][0]['snippet']['tags']
        except KeyError:
            tags = []
        # print(tags)
        print(title)
        try:
            view_count = res['items'][0]['statistics']['viewCount']
        except KeyError:
            view_count = 0
        try:
            like_count = res['items'][0]['statistics']['likeCount']
        except KeyError:
            like_count = 0
        try:
            dislike_count = res['items'][0]['statistics']['dislikeCount']
        except KeyError:
            dislike_count = 0
        try:
            favorite_count = res['items'][0]['statistics']['favoriteCount']
        except KeyError:
            favorite_count = 0
        try:
            comment_count = res['items'][0]['statistics']['commentCount']
        except KeyError:
            comment_count = 0

        # print(tags)
        if YoutubeVideo.objects.filter(channel=channel_object, video_id=video_id).exists():
            previous_view_count = YoutubeVideo.objects.filter(channel=channel_object,
                                                              video_id=video_id).first().view_count
            increased_view_count = int(view_count) - previous_view_count
            YoutubeVideo.objects.filter(channel=channel_object, video_id=video_id).update(
                title=title,
                published_at=published_at,
                previous_view_count=previous_view_count,
                increased_view_count = increased_view_count,
                view_count=view_count, like_count=like_count,
                dislike_count=dislike_count,
                favorite_count=favorite_count,
                comment_count=comment_count)
        else:
            YoutubeVideo.objects.create(channel=channel_object, video_id=video_id,
                                        title=title,
                                        published_at=published_at,
                                        view_count=view_count, like_count=like_count,
                                        dislike_count=dislike_count,
                                        favorite_count=favorite_count,
                                        comment_count=comment_count)
        if tags:
            YoutubeVideo.objects.filter(channel=channel_object, video_id=video_id).first().tags.set(*tags)

    channel_object.save()


def get_channel_videos(request, channel_id):
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_id,
                                  part='contentDetails,snippet,statistics').execute()
    title = res['items'][0]['snippet']['title']
    published_at = res['items'][0]['snippet']['publishedAt']
    view_count = res['items'][0]['statistics']['viewCount']
    subscriber_count = res['items'][0]['statistics']['subscriberCount']
    video_count = res['items'][0]['statistics']['videoCount']

    if YoutubeChannel.objects.filter(channel_id=channel_id).exists():
        YoutubeChannel.objects.filter(channel_id=channel_id).update(title=title, view_count=view_count,
                                                                    subscriber_count=subscriber_count,
                                                                    video_count=video_count, published_at=published_at)
    else:
        YoutubeChannel.objects.create(
            channel_id=channel_id, title=title, view_count=view_count, subscriber_count=subscriber_count,
            video_count=video_count, published_at=published_at
        )

    # print(res)
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None

    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='contentDetails',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    # return videos
    # videos = get_channel_videos(channel_id)
    video_ids = list(map(lambda x: x['contentDetails']['videoId'], videos))
    get_videos_stats(video_ids, channel_id)
    return HttpResponse("Fetch Successfully")
