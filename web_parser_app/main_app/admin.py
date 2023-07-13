from django.contrib import admin
from .models import Video, VideoGroup


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(VideoGroup)
class VideoGroupAdmin(admin.ModelAdmin):
    pass