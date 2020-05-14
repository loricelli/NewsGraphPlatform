from django.db import models

from django.contrib.auth.models import User

class Voter(models.Model):
    points = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def increase_points(self):
        self.points += 1
        self.save()
