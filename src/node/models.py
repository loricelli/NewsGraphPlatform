from django.db import models

from news.models import News
from edge.models import Edge

from django.db.models import Q

class Node(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    color = models.CharField(max_length=10,default="violet")

    def check_all_confirm(self):
        in_edges = Edge.objects.filter(head=self)
        conf_in_edges = in_edges.filter(~Q(stance=-1))
        return len(in_edges) == len(conf_in_edges)

    def color_node(self):

        in_edges = Edge.objects.filter(head=self)

        if is_admissible(in_edges):
            if len(in_edges) == 1:
                self.color = color_simple_case(in_edges[0])
            else:
                colors = set()
                for edge in list(in_edges):
                    color = color_simple_case(edge)
                    colors.add(color)
                    print(colors)

                if 'yellow' in list(colors) and 'green' in list(colors):
                    self.color = 'gray'
                else:
                    self.color = list(colors)[0]

            self.save()
        else:
            self.delete()

def color_simple_case(edge):
    discuss = 0
    agree = 1
    disagree = 2
    stance = edge.stance
    tail = edge.tail
    if stance == discuss:
        if tail.color == 'gray':
            return 'gray'
        elif tail.color == 'black' or tail.color == 'yellow':
            return 'yellow'
        elif tail.color == 'white' or tail.color == 'green':
            return 'green'
    elif stance == agree:
        if tail.color == 'black' or tail.color == 'yellow':
            return 'black'
        elif tail.color == 'white' or tail.color == 'green':
            return 'white'
    elif stance == disagree:
        if tail.color == 'black' or tail.color == 'yellow':
            return 'white'
        elif tail.color == 'white' or tail.color == 'green':
            return 'black'

def get_tails_subsets(edges):
  B,W,G = list(),list(),list()

  for edge in edges:
    tail_color = edge.tail.color
    if tail_color in ['black','yellow']:
      B.append(edge)
    elif tail_color in ['white','green']:
      W.append(edge)
    else:
      G.append(edge)
  return B,W,G

def all_discuss(edges):
  for edge in edges:
    if edge.stance is not 0:
      return False
  return True

def all_same_label(edges):
  last_seen = None
  for edge in edges:
    if not last_seen:
      last_seen = edge.stance
    elif edge.stance != last_seen:
      return False
  return True

def all_confirm_disc(edges):
  for edge in edges:
    if edge.stance not in [0,1]:
      return False
  return True

def all_confutations(edges):
  for edge in edges:
    if edge.stance is not 2:
      return False
  return True


def is_admissible(edges):
  B,W,G = get_tails_subsets(edges)
  if len(G) > 0:
    if (len(B) > 0 and not all_discuss(B)) or (len(W) > 0 and not all_discuss(W)) or not all_discuss(G):
      return False
  else:
    if len(B) > 0 and len(W) == 0:
      if not all_same_label(B) and not all_confirm_disc(B):
        return False
    elif len(B) == 0 and len(W) > 0:
      if not all_same_label(W) and not all_confirm_disc(W):
        return False
    elif len(B) > 0 and len(W) > 0:
      if (not all_confutations(B) or not all_confirm_disc(W)) and (not all_confutations(W) or not all_confirm_disc(B)) and (not all_discuss(B) or not all_discuss(W)):
        return False
  return True
