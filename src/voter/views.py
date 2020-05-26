from django.shortcuts import render,redirect
from django.contrib import messages
from datetime import datetime, timezone
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json
from math import ceil
from django.contrib.auth.decorators import login_required

@login_required(login_url='/signin/')
def profile_page(request, *args, **kwargs):
    if request.user.is_authenticated:
        now = datetime.now(timezone.utc)
        voter = request.user.voter
        n_confirm = voter.confirmation_set.count()
        points = voter.points
        confirmations = voter.confirmation_set.all().order_by('-id')[:5]
        last_act = [vote_to_text(c.vote) for c in confirmations]
        diff_time = [days_hours_minutes(now,conf.date) for conf in confirmations]

        month_confirmations = voter.confirmation_set.all().filter(date__month=datetime.now().month)
        count_array = month_confirmations.values('date__date').annotate(dcount=Count('date__date'))
        count_array = pad_dates(count_array)
        count_json = json.dumps(list(count_array),cls=DjangoJSONEncoder)

        context = {
            'confirmations': n_confirm,
            'points': points,
            'last_act': zip(last_act,diff_time),
            'count_array': count_json,
            'read_time': ceil(voter.reading_time),
            'streak': voter.streak

        }
        return render(request,"voters/profile.html",context)
    else:
        messages.warning(request, "You must be logged in!")
        return redirect('home')


def days_hours_minutes(now,date):
    delta = now - date
    return delta.days, delta.seconds//3600, (delta.seconds//60)%60

def vote_to_text(vote):
    if vote == 0:
        return 'Discuss'
    elif vote == 1:
        return 'Agree'
    elif vote == 2:
        return 'Disagree'


from datetime import date, timedelta
from operator import itemgetter

def pad_dates(count_array):
    today = date.today()
    bg = date(today.year,today.month,1)

    time_delta = today - bg
    entry_list = list(count_array)
    for i in range(time_delta.days +1):
        dates_list = [l['date__date'] for l in entry_list]
        day = bg + timedelta(days=i)
        if day not in dates_list:
            entry_list.append({'date__date':day,'dcount':0})
    entry_list.sort(key=itemgetter('date__date'))
    return entry_list


