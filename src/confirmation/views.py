from django.shortcuts import redirect
from voter.models import Voter
from edge.models import Edge
from .models import Confirmation



def create_confirmation(request, *args, **kwargs):
    voter = Voter.objects.get(user=request.user)
    vote = kwargs['vote']
    edge = Edge.objects.get(id=kwargs['edge_id'])
    Confirmation.objects.create(edge=edge,vote=vote,voter=voter)

    return redirect("/")
