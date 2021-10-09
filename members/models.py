from django.db import models

# Create your models here.

class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    display_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    birth_date = models.DateField()

    # gender = models. (max_length=64)
    # set_lists = models.CharField(max_length=64)

    # class Meta:
    #     def full_name(self):
    #         return f"{self.first_name} {self.last_name}"


# class Group(models.Model):
#     name = models.CharField(max_length=256)
#     members = models.ManyToManyField(Person)

#     class Meta:
#         ordering = ['name']

#         def __str__(self):
#             return self.title


# class Instruments(models.Model):
#     name = models.CharField(max_length=64)
