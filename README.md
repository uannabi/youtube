# youtube
## Installation steps:
  - virtualenv y-env 
  - source y-env/bin/activate
  - gh repo clone uannabi/youtube 
  - pip install -r requirements.txt
  - goto youtube/api/fetch_youtube_data.py line number 5, put api key
  - python manage.py runserver 
  - to fetch video content http://localhost:8000/channel/chnnel_id_here
  - to see video list http://localhost:8000/videos
  - to filter video by tage http://localhost:8000/videos?tag=buet
  - to filter video by perfomance http://localhost:8000/videos?performance=2000
