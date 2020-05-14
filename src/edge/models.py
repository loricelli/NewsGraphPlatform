from django.db import models
from django.db.models import Q
import random


class Edge(models.Model):
    tail = models.ForeignKey("node.Node", on_delete=models.CASCADE, related_name='tail')
    head = models.ForeignKey("node.Node", on_delete=models.CASCADE, related_name='head')
    color = models.CharField(max_length=7,default="#000000")
    stance = models.IntegerField(default=-1)


    def __str__(self):
        return str(self.tail)+ "-->"+str(self.head)

    @classmethod
    def get_random_edge(self):
        default_color = "violet"
        edges_list = self._meta.model.objects.filter(~Q(tail__color=default_color),head__color=default_color,stance=-1)
        if edges_list:
            random_edge = random.choice(edges_list)
            return random_edge
        else:
            return edges_list

    def color_edge(self):
        discuss = 0
        agree = 1
        disagree = 2
        stance = self.stance
        tail_source = self.tail.news.source
        head_source = self.head.news.source
        if stance == agree:
            if tail_source != head_source:
                self.color = "#196b0e"
            else:
                self.color = "#72ed61"
        elif stance == disagree:
            if tail_source != head_source:
                self.color = "#bf0404"
            else:
                self.color = "#fa7b0c"
        elif stance == discuss:
            self.color = "#0b40d4"
        self.save()


