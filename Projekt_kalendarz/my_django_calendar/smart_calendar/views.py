from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from calendar import monthrange
from datetime import datetime, timedelta
from .models import Event
from .forms import EventForm
from datetime import datetime, timedelta
from calendar import monthrange, weekday
from django.http import JsonResponse

import requests

def weather_info(city):
    API_KEY = 'YOUR_API_KEY'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pl'

    resp = requests.get(url)

    if resp.status_code == 200:
        resp_data = resp.json()
        temperature = round(resp_data['main']['temp'], 1)

        weather_data ={
            'city': resp_data['name'],
            'temperature': temperature,
            'description': resp_data['weather'][0]['description'],
        }
        return weather_data
    else:
        return None

def home(request):
    context = {}
    if request.user.is_authenticated:
        username = request.user.username
        context['userStatus'] = 'LOG IN'
        context['user'] = username
    else:
        context['userStatus'] = 'Not authenticated'
    return render(request, 'home.html', context)

def user_login(request): 
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_user = authenticate(request, username=username, password=password)
        if login_user is not None:
            login(request, login_user)
            return redirect('calendar')
        else:
            context['error'] = "Invalid Credentials"
    return render(request, 'login.html', context)

def user_signup(request): 
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password_1 = request.POST.get('password')
        password_2 = request.POST.get('confirm_password')
        
        if not username or not password_1 or not password_2:
            context['error'] = 'All fields are required'
            return render(request, 'signup.html', context)
        
        try: #Użytkownik istnieje w bazie danych
            user = User.objects.get(username=username)
            context['error'] = 'The username you have entered already exists.'
            return render(request, 'signup.html', context)
        
        except User.DoesNotExist:
            if password_1 != password_2:
                context['error'] = 'Passwords don\'t match.'
                return render(request, 'signup.html', context)
            else:
                correct_user = User.objects.create_user(username, password=password_1)
                auth.login(request, correct_user)
                return redirect('home')     
    else:
        return render(request, 'signup.html', context)
         
@login_required       
def user_logout(request): 
    logout(request)
    return redirect('login')

def calendar_main(request):
    today = datetime.today()
    month = request.GET.get('month', today.month)
    year = request.GET.get('year', today.year)
    
    month = int(month)
    year = int(year)

    # Obliczanie dni w miesiącu
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = monthrange(year, month)[1]
    days = [first_day_of_month + timedelta(days=i) for i in range(last_day_of_month)]

    #Filtrowanie wydarzeń tylko dla zalogowanego użytkownika 
    events = Event.objects.filter(user=request.user, date__year=year, date__month=month)
    
    city = 'your_hometown_name'
    weather_data = weather_info(city)

    if weather_data is None:
        weather_data = {
            'name': city,
            'main': {
                'temp': 'No data',
                'humidity': 'No data',
            },
            'weather': [{'description': 'No data'}],
            'wind': {'speed': 'No data'}
        }

    context = {
        'month': month,
        'year': year,
        'days': days,
        'events': events,
        'weather': weather_data
    }
    return render(request, 'calendar_main.html', context)

def get_calendar_days(request):
    current_date = datetime.now()

    month = int(request.GET.get('month', current_date.month))
    year = int(request.GET.get('year', current_date.year))

    # Obliczanie dni w miesiącu
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = monthrange(year, month)[1]
    
    prev_month_last_day = first_day_of_month - timedelta(days=1)
    prev_month_days = prev_month_last_day.day
    prev_days = [
        {'day': prev_month_last_day.replace(day=prev_month_days - i).day, 'current_month': False} 
        for i in range(first_day_of_month.weekday())
    ]

    # Obecne dni (z bieżącego miesiąca)
    current_days = [
        {'day': day, 'current_month': True} 
        for day in range(1, last_day_of_month + 1)
    ]

    # Następne dni (z następnego miesiąca)
    next_days_count = 6 - datetime(year, month, last_day_of_month).weekday()
    next_days = [
        {'day': i + 1, 'current_month': False} 
        for i in range(next_days_count)
    ]

    days = prev_days + current_days + next_days

    events = Event.objects.filter(user=request.user, date__year=year, date__month=month)
    events_formatted = [{'title': event.title, 'description': event.description, 'date': event.date.day} for event in events]

    return JsonResponse({'days': days, 'events': events_formatted, 'month': month, 'year': year})

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save(user=request.user) # Przekazanie zalogowanego użytkownika do formularza
            print(f"Dodano event:")
            return redirect('calendar')
    else:
        form = EventForm()
    return render(request, 'add_event.html')

@login_required
def del_event(request, event_id):
    print(f"Rozpoczynanie del eventu")
    event = Event.objects.get(title=event_id, user=request.user)
    print(f"{event_id}")
    event.delete()
    return redirect('calendar')
