from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date']

    def save(self, user=None, *args, **kwargs): #Przypisanie zalogowanego usera od tworzonego wydarzenia
        instance = super(EventForm, self).save(commit=False)
        if user:
            instance.user = user
        instance.save()
        return instance

