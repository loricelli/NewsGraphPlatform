from django.shortcuts import render,redirect
from edge.models import Edge
from django.db import transaction,IntegrityError
from django.contrib import messages


def tail_news(request, *args, **kwargs):
    if request.user.is_authenticated:
        try:
            with transaction.atomic():
                edge = Edge.get_random_edge()
        except IntegrityError:
            edge = []

        if edge:
            context = {
                'edge':edge
            }
            return render(request,"nodes/news_read.html",context)
        else:
            messages.info(request, "No news available! Try later.")
            return redirect("/")
    else:
        messages.warning(request, "You must be logged in!")
        return redirect("/")

def head_news(request, *args, **kwargs):
    context = {
        'edge':Edge.objects.get(id=kwargs['edge_id'])
    }
    return render(request,"nodes/news_compare.html",context)
