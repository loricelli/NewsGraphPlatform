from django.db import models
from voter.models import Voter
from edge.models import Edge
from django.db.models.signals import post_save
from collections import Counter

max_confirmations = 1

class Confirmation(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    edge = models.ForeignKey(Edge, on_delete=models.CASCADE)
    vote = models.IntegerField()

def check_stance(edge):
    confirmations = Confirmation.objects.filter(edge=edge)
    if len(confirmations) >= max_confirmations:
        #TODO pareggio
        votes = [conf.vote for conf in confirmations]
        counter = Counter(votes)
        most_common = counter.most_common(1)
        return most_common[0][0]
    return None




def save_confirmation(sender, instance, **kwargs):
    ret = check_stance(instance.edge)
    print(instance.edge, ret)
    if ret is not None:
        edge = instance.edge
        edge.stance = ret
        edge.save()
        edge.color_edge()
        assign_points(edge)
        if edge.head.check_all_confirm():
            edge.head.color_node()

def assign_points(edge):
    confirmations = edge.confirmation_set.all()

    for conf in confirmations:
        if conf.vote == edge.stance:
            conf.voter.increase_points()




post_save.connect(save_confirmation, sender=Confirmation)



