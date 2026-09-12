from django.conf import settings
from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    comment = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_meetings'
    )
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='meetings', blank=True)

    class Meta:
        ordering = ['start']

    def __str__(self):
        return f'{self.title} ({self.start:%Y-%m-%d %H:%M})'

    def can_edit(self, user):
        return user.is_staff or self.created_by_id == user.id
