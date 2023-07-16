from django.urls import path
from .views import start_parsing, settings

app_name = 'parser_service'
urlpatterns = [
    path('', start_parsing, name='parsing'),
    path('settings', settings, name='settings'),
]
