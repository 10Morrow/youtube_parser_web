from django.urls import path
from .views import video_list_view, start_parsing, return_playlist_by_id

app_name = 'main_app'
urlpatterns = [
    path('', video_list_view, name='video_list'),
    path('data/<slug:identifier>', return_playlist_by_id, name='identifier'),
    path('start_parsing', start_parsing, name='start_parsing'),
]