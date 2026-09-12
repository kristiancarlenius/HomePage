from django.conf import settings
from django.db import models


class RepoLink(models.Model):
    TAG_CHOICES = [('ours', 'Ours'), ('external', 'External')]

    name = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='ours')
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='repo_links'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['tag', 'name']

    def __str__(self):
        return self.name
