from django.shortcuts import render,redirect
from edge.models import Edge
from django.db import transaction,IntegrityError
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.views.decorators.cache import never_cache

AVG_READ_TIME = 200

@never_cache
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
            news_words = len(re.findall(r'\w+', edge.tail.news.body))
            request.user.voter.reading_time += news_words/AVG_READ_TIME
            request.user.voter.save()

            return render(request,"nodes/news_read.html",context)
        else:
            messages.info(request, "No news available! Try later.")
            return redirect("/")
    else:
        messages.warning(request, "You must be logged in!")
        return redirect("/")

@never_cache
@login_required(login_url='/signin/')
def head_news(request, *args, **kwargs):
    edge = Edge.objects.get(id=kwargs['edge_id'])
    context = {
        'edge':edge
    }
    news_words = len(re.findall(r'\w+', edge.head.news.body))
    request.user.voter.reading_time += news_words/AVG_READ_TIME
    request.user.voter.save()
    return render(request,"nodes/news_compare.html",context)

@csrf_exempt
def leave_page(request, *args, **kwargs):
    edge = request.POST.get('edge_id')
    edge_obj = Edge.objects.get(pk=edge)
    edge_obj.usr_reading -= 1
    edge_obj.save()
    return HttpResponse(status=302)



