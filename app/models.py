from datetime import datetime
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
import pytz


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Article(models.Model):
    name = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    image_url = models.CharField(max_length=100)
    description = models.TextField()
    available = models.BooleanField(default=True)
    final_price = models.FloatField(default=0)
    expiry = models.DateTimeField(
        default=(datetime.datetime.now() + datetime.timedelta(days=30)).replace(
            tzinfo=pytz.UTC
        )
    )

    def __str__(self) -> str:
        return self.name


class Offer(models.Model):
    referring_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=False
    )
    referring_article = models.ForeignKey(
        Article, on_delete=models.CASCADE, blank=True, null=False
    )
    price = models.FloatField(default=0)
    datetime = models.DateTimeField(
        default=datetime.datetime.now().replace(tzinfo=pytz.UTC)
    )
