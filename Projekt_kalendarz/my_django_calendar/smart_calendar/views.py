from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def home(request):
    return render(request, 'home.html')

def user_login(request):
    return render(request, 'login.html')

def user_signup(request):
    return render(request, 'signup.html')

def user_logout(request):
    return render(request, 'logout.html')    
