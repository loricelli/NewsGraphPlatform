from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
import json

from edge.models import Edge
from node.models import Node
from source.models import Source
from voter.models import Voter
from django.db.models import Q
from pages.forms import CreateVoterForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from datetime import date,timedelta
import networkx as nx

def home_view(request, *args, **kwargs):


    fake_nodes = Node.objects.filter(fake=True)
    fake_news = [( node.news.title,node.news.source.name ) for node in fake_nodes]

    edges = Edge.objects.all()
    nodes = Node.objects.all()

    dict_edges = [model_to_dict(obj) for obj in edges]
    dict_nodes = [model_to_dict(obj) for obj in nodes]

    reliability = dict()
    for source in Source.objects.all():
        reliability[source.name] = source.reliability

    reliability = {k: v for k, v in sorted(reliability.items(), key=lambda x: x[1],reverse=True)}
    print(reliability)
    ser_edges = json.dumps(dict_edges)
    ser_nodes = json.dumps(dict_nodes)
    context = {
        "edges":ser_edges,
        "nodes":ser_nodes,
        "tot_news": Node.objects.count(),
        "tot_usr": Voter.objects.count(),
        "an_news": Node.objects.filter(~Q(color="violet")).count(),
        "fake_news": fake_news,
        "source_reliability": reliability
    }
    return render(request,'home.html',context)


def signup(request):
    form = CreateVoterForm()
    context = {
        "form": form
    }

    if request.method == 'POST':
        form = CreateVoterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/signin')
        else:
            return render(request,'signup.html',{'form':form})

    return render(request,'signup.html',context)

def signin(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=uname, password=pwd)

        if user is not None:

            if user.last_login:
                today = date.today()
                yesterday = today - timedelta(days=1)

                last_login = user.last_login.date()
                if last_login < yesterday:
                    user.voter.streak = 1
                    user.voter.save()
                elif last_login == yesterday:
                    user.voter.streak += 1
                    user.voter.save()

            login(request,user)
            messages.success(request, uname + ' succesfully logged in!')
            return redirect('/')
        else:
            messages.error(request, "Username or password are not correct! Please retry.")
            return render(request,'signin.html')
    context = {}
    return render(request,'signin.html',context)

def signout(request):
    logout(request)
    messages.success(request,'Succesfully logged out!')
    return redirect('home')
