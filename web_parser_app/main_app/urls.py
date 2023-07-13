from django.urls import path
from .views import video_list_view, start_parsing

urlpatterns = [
    path('', video_list_view, name='video_list'),
    path('start_parsing', start_parsing, name='start_parsing'),
]