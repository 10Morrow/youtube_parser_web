from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('parsing/', include('parser_service.urls')),
]