from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User

from .models import Subject, NoFactToLearn, NoCardToLearn, get_memorised_cards, Memory

def home_page(request):
    subjects = Subject.objects.all()
    context = { 'subjects' : subjects }
    return render(request, 'home.html', context)

def study(request, subject_id):
    if not request.user.is_authenticated: return render(request, 'please_login.html')

    subject = get_object_or_404(Subject, id=subject_id)
    context = {'title':subject.title}

    try:
        memory = subject.get_next_card(request.user)
    except NoCardToLearn:
        return render(request, 'no_cards_to_learn.html', context)
    except NoFactToLearn:
        return render(request, 'no_fact_to_learn.html', context)
    try:
        if request.session['memory2rate'] != None:
            memory_id = request.session['memory2rate']
            memory = get_object_or_404(Memory, id=memory_id, user=request.user)
            #print (memory.card.fact.order)
    except KeyError:
        pass
    to_be_repeated, other = get_memorised_cards(request.user, subject)
    #info = {'to_repeat': to_be_repeated,
    #        'other' : other}


    context.update(memory.card.format_card())
    #context.update(info)


    if request.method == "POST":
        context.update({'show_question': False})
        score = request.POST.get("rate", None)
        #print(context['front'])
        if score in ['-1','0','+1']:
            memory.rate(int(score))
            request.session['memory2rate'] = None
            return HttpResponseRedirect(request.path)
        else:
            return render(request, 'study.html', context)
    else:
        #print(context['front'])
        context.update({'show_question': True})
        request.session['memory2rate'] = memory.id
        return render(request, 'study.html', context)

def study_list(request):
    subjects = Subject.objects.all()
    context = { 'subjects' : subjects }
    return render(request, 'study_list.html', context)

