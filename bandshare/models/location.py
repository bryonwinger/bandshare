from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=256, default="")
    address = models.CharField(blank=True, max_length=256)
    state = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(null=True, max_length=10)
    country = models.CharField(max_length=64, default='United States of America')

    def __str__(self):
        return self.postal_code

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['address', 'city', 'state', 'postal_code', 'country'], name='unique_location')
        ]

