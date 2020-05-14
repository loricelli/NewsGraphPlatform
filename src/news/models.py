from django.db import models
from source.models import Source

class News(models.Model):
    news_id = models.IntegerField()
    title = models.TextField()
    body  = models.TextField(blank=True,null=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.news_id)
