from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Voter(models.Model):
    points = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reading_time = models.FloatField(default=0.0)
    streak = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

    def increase_points(self):
        self.points += 1
        self.save()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Voter.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
