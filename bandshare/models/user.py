from django.db import models
from django.utils.timezone import now

from dateutil import relativedelta

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    display_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    birth_date = models.DateField(null=True)
    description = models.CharField(max_length=512, default='', blank=True)
    bio = models.CharField(max_length=4096, default='', blank=True)

    groups = models.ManyToManyField('Group')
    genres = models.ManyToManyField('Genre')
    instruments = models.ManyToManyField('Instrument', blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def age(self):
        "Returns the number of years between birth_date and today."
        today = now().date()
        delta = relativedelta.relativedelta(today, self.birth_date)
        return delta.years

    @property
    def full_name(self):
        "Returns the full name."
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
