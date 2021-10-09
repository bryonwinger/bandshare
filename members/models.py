from django.db import models
from django.utils.timezone import now

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    display_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    birth_date = models.DateField(null=True)
    genres = models.ManyToManyField(Genre)
    
    @property
    def full_name(self):
        "Returns the full name."
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    # gender = models.OneToOneField(Gender)
    # set_lists = models.CharField(max_length=64)


class Group(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_date = models.DateField(default=now)

    name = models.CharField(max_length=256)
    members = models.ManyToManyField(User)
    genres = models.ManyToManyField(Genre)


# class Instrument(models.Model):
#    name = models.CharField(max_length=64)
