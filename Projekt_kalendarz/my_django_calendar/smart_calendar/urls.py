from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('calendar_main/', views.calendar_main, name='calendar'),
    path('get_calendar_days/', views.get_calendar_days, name='get_calendar_days'),
    path('add_event/', views.add_event, name='add_event'),
    path('del_event/<int:event_id>/', views.del_event, name='del_event')
]
