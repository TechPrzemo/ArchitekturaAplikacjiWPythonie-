from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    event_id = models.IntegerField()

    def __str__(self):
        return self.title

# Create your models here.
