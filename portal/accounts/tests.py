from django.test import TestCase
from django.urls import reverse

from .models import User


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pw12345!')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_when_logged_in(self):
        self.client.login(username='alice', password='pw12345!')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
