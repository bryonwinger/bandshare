from django.db import models
from django.utils.timezone import now

class Group(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_date = models.DateField(default=now)
    created_by = models.ForeignKey('User', related_name='created_by', on_delete=models.CASCADE)
    owned_by = models.ForeignKey('User', related_name='owned_by', on_delete=models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, blank=True)
    bio = models.CharField(max_length=4096, blank=True)

    members = models.ManyToManyField('User', through='GroupMembership')
    genres = models.ManyToManyField('Genre')
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def member_roles(self):
        """Returns a list of each User and their roles."""
        return [{'user': gm.member, 'role': gm.role} for gm in self.groupmembership_set.all()]


class GroupMembership(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    member = models.ForeignKey('User', on_delete=models.CASCADE)
    role = models.CharField(max_length=128)
