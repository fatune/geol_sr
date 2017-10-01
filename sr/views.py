from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .models import Subject, NoFactToLearn, NoCardToLearn

def home_page(request):
    return render(request, 'home.html')

def study(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    context = {'title':subject.title}
    try:
        next_card = subject.get_next_card(request.user)
    except NoCardToLearn:
        return render(request, 'no_cards_to_learn.html', context)
    except NoFactToLearn:
        return render(request, 'no_fact_to_learn.html', context)

    context.update(next_card.format_card())
    return render(request, 'study.html', context)



