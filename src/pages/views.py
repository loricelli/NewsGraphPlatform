from django.shortcuts import render
from django.forms.models import model_to_dict
import json

from edge.models import Edge
from node.models import Node

def home_view(request, *args, **kwargs):

    dict_edges = [model_to_dict(obj) for obj in Edge.objects.all()]
    dict_nodes = [model_to_dict(obj) for obj in Node.objects.all()]
    ser_edges = json.dumps(dict_edges)
    ser_nodes = json.dumps(dict_nodes)
    return render(request,"home.html",{"edges":ser_edges,"nodes":ser_nodes})

