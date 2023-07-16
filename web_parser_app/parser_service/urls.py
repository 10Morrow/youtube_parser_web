from django.urls import path
from .views import start_parsing

app_name = 'parser_service'
urlpatterns = [
    path('', start_parsing, name='parsing'),
]
