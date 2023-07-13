from django.db import models
import string
import random

class Video(models.Model):
    video_link = models.CharField(max_length=200)
    views = models.PositiveIntegerField()
    subscribers = models.PositiveIntegerField()
    monetized = models.BooleanField()

    def __str__(self):
        return self.video_link


def generate_unique_identifier():
    characters = string.ascii_uppercase + string.digits
    while True:
        identifier = ''.join(random.choice(characters) for _ in range(7))
        if not VideoGroup.objects.filter(identifier=identifier).exists():
            return identifier


class VideoGroup(models.Model):
    identifier = models.CharField(max_length=7, unique=True, default=generate_unique_identifier)
    created_at = models.DateTimeField(auto_now_add=True)
    videos = models.ManyToManyField(Video)

    def __str__(self):
        return self.identifier
