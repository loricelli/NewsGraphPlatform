from django.db import models
from voter.models import Voter
from edge.models import Edge

class Confirmation(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    edge = models.ForeignKey(Edge, on_delete=models.CASCADE)
    vote = models.IntegerField()


