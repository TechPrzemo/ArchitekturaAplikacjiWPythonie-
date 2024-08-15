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
def user_logout(request): #Zeby można było po zalogowaniu się wylogować 
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

    events = Event.objects.filter(date__year=year, date__month=month)
    
    context = {
        'month': month,
        'year': year,
        'days': days,
        'events': events,
    }
    return render(request, 'calendar_main.html', context)

def get_calendar_days(request):
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))

    # Obliczanie dni w miesiącu
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = monthrange(year, month)[1]
    days = [first_day_of_month + timedelta(days=i) for i in range(last_day_of_month)]

    days_formatted = [{'day': day.day, 'weekday': day.strftime('%A')} for day in days]

    events = Event.objects.filter(date__year=year, date__month=month)
    events_formatted = [{'title': event.title, 'description': event.description, 'date': event.date.day} for event in events]

    return JsonResponse({'days': days_formatted, 'events': events_formatted, 'month': month, 'year': year})

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            print(f"Dodano event:")
            return redirect('calendar')
        
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

def del_event(request, event_id):
    print(f"Rozpoczynanie del eventu")
    event = Event.objects.get(id=event_id)
    print(f"{event_id}")
    event.delete()
    return redirect('calendar')