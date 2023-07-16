from django.contrib import admin
from .models import Mode, PersonSettings


@admin.register(Mode)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(PersonSettings)
class VideoGroupAdmin(admin.ModelAdmin):
    pass