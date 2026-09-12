from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import RepoLink


class RepoLinkTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pw12345!')

    def test_list_requires_login(self):
        response = self.client.get(reverse('repo_list'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_add_repo(self):
        self.client.login(username='alice', password='pw12345!')
        response = self.client.post(
            reverse('repo_create'),
            {'name': 'HomePage', 'url': 'https://github.com/kristiancarlenius/HomePage', 'tag': 'ours', 'description': ''},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RepoLink.objects.count(), 1)
