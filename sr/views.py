from django.shortcuts import render, redirect

def home_page(request):
    return render(request, 'home.html')

def study(request, subject_id):
    return render(request, 'home.html')

