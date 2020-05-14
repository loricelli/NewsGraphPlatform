from django.db import models

from news.models import News

from django.db.models import Q

class Node(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    color = models.CharField(max_length=10,default="violet")
