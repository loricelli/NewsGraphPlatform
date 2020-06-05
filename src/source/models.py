from django.db import models

class Source(models.Model):
    name = models.TextField()
    reliability = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
