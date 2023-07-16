from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Mode(models.Model):
    mode_id = models.CharField(max_length=255, unique=True)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return self.comment


class PersonSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    words_file = models.FileField(upload_to='media/')
    min_view_count = models.IntegerField(default=100000, validators=[MinValueValidator(20000),
                                                                    MaxValueValidator(1000000)])
    shorts = models.BooleanField(default=False)
    max_sub_count = models.IntegerField(default=20000, validators=[MinValueValidator(2000),
                                                                   MaxValueValidator(1000000)])
    proxy_address = models.CharField(max_length=255, null=True, blank=True)
    proxy_login = models.CharField(max_length=255, null=True, blank=True)
    proxy_pass = models.CharField(max_length=255, null=True, blank=True)
    mode = models.ForeignKey(Mode, on_delete=models.PROTECT)
