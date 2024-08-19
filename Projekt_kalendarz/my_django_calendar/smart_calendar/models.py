from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Pole wskazujące który użytkownik utworzył dany event

    def __str__(self):
        return self.title






