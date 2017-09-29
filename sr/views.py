from django.shortcuts import render, redirect, get_object_or_404

from .models import Subject

def home_page(request):
    return render(request, 'home.html')

def study(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'study.html')

