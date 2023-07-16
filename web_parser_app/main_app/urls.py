from django.urls import path
from .views import video_identifiers_view, return_playlist_by_id, main_page_view, settings

app_name = 'main_app'
urlpatterns = [
    path('', main_page_view, name='main_page'),
    path('settings', settings, name='settings'),
    path('parsed_data', video_identifiers_view, name='parsed_data'),
    path('parsed_data/<slug:identifier>', return_playlist_by_id, name='identifier'),
]
