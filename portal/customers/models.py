from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    contact_info = models.TextField(blank=True, help_text='Contact person, email, phone, etc.')
    rate = models.CharField(max_length=100, blank=True, help_text='e.g. hourly rate or monthly fee')
    projects_done = models.TextField(blank=True, help_text='Projects we have delivered for them')
    potential_needs = models.TextField(blank=True, help_text='What we think they might need next')
    known_issues = models.TextField(blank=True, help_text='Problems we are aware of')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
