from django.shortcuts import render,redirect
from edge.models import Edge

def tail_news(request, *args, **kwargs):
    edge = Edge.get_random_edge()

    if edge:
        context = {
            'edge':edge
        }
        return render(request,"nodes/news_read.html",context)
    else:
        return redirect("/")

def head_news(request, *args, **kwargs):
    context = {
        'edge':Edge.objects.get(id=kwargs['edge_id'])
    }
    return render(request,"nodes/news_compare.html",context)
