from django.db import models
from django.db.models import Q,F
from django.db.models.signals import post_delete
import random

default_color = "violet"

self_confirm_color = "#72ed61"
confirm_color = "#196b0e"
discuss_color = "#0b40d4"
self_disagree_color = "#fa7b0c"
disagree_color = "#bf0404"

max_confirmations = 1

class Edge(models.Model):
    tail = models.ForeignKey("node.Node", on_delete=models.CASCADE, related_name='tail')
    head = models.ForeignKey("node.Node", on_delete=models.CASCADE, related_name='head')
    color = models.CharField(max_length=7,default="#000000")
    stance = models.IntegerField(default=-1)
    usr_reading = models.IntegerField(default=0)
    n_confirmations = models.IntegerField(default=0)



    def __str__(self):
        return str(self.tail)+ "-->"+str(self.head)

    @classmethod
    def get_random_edge(self,user):
        edges_list = self._meta.model.objects.filter(~Q(tail__color=default_color),head__color=default_color,stance=-1,usr_reading__lt=max_confirmations-F("n_confirmations"))

        if edges_list:
            tmp_edges_list = list(edges_list)
            while tmp_edges_list:
                random_edge = random.choice(tmp_edges_list)
                edge_conf_set = set(random_edge.confirmation_set.all())
                user_conf_set = set(user.voter.confirmation_set.all())
                if edge_conf_set.intersection(user_conf_set) == set():
                    random_edge.usr_reading += 1
                    random_edge.save()
                    return random_edge
                else:
                    tmp_edges_list.remove(random_edge)
            return [] #all edges already have a voter confirmation. He can't confirm twice
        else:
            return  []

    def color_edge(self):
        discuss = 0
        agree = 1
        disagree = 2
        stance = self.stance
        tail_source = self.tail.news.source
        head_source = self.head.news.source
        if stance == agree:
            if tail_source != head_source:
                self.color = confirm_color
            else:
                self.color = self_confirm_color
        elif stance == disagree:
            if tail_source != head_source:
                self.color = disagree_color
            else:
                self.color = self_disagree_color
        elif stance == discuss:
            self.color = discuss_color
        self.save()


"""
After an unrelated edge is deleted we have to check if its nodes are implied in other edges.
It that's not the case, we delete the news and node too, to free space.
If one of the node is paired with other edges we have to check for potential coloring issues.
"""
def evaluate_node(node):
    in_edges = Edge.objects.filter(head=node)
    out_edges = Edge.objects.filter(tail=node)

    if not in_edges and not out_edges:
        node.delete()
    elif not in_edges and out_edges:
        node.color = 'black'
        node.save()

def unrelated_deleted(sender, instance, **kwargs):
    tail = instance.tail
    head = instance.head

    evaluate_node(tail)
    evaluate_node(head)



post_delete.connect(unrelated_deleted, sender=Edge)

