from django.db import models

class Edge(models.Model):
    tail = models.ForeignKey("node.Node", on_delete=models.CASCADE, related_name='tail')
    head = models.ForeignKey("node.Node", on_delete=models.CASCADE, related_name='head')
    color = models.CharField(max_length=7,default="#000000")
    stance = models.IntegerField(default=-1)


    def __str__(self):
        return str(self.tail)+ "-->"+str(self.head)


