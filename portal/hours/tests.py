from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import TimeEntry


class HoursPermissionTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pw12345!')
        self.bob = User.objects.create_user(username='bob', password='pw12345!')
        self.admin = User.objects.create_user(username='kristian', password='pw12345!', is_staff=True)
        self.alice_entry = TimeEntry.objects.create(user=self.alice, date='2026-01-01', hours=3)

    def test_my_hours_only_shows_own_entries(self):
        TimeEntry.objects.create(user=self.bob, date='2026-01-02', hours=5)
        self.client.login(username='alice', password='pw12345!')
        response = self.client.get(reverse('my_hours'))
        self.assertContains(response, '2026-01-01')
        self.assertNotContains(response, '2026-01-02')

    def test_user_cannot_edit_another_users_entry(self):
        self.client.login(username='bob', password='pw12345!')
        response = self.client.get(reverse('entry_edit', args=[self.alice_entry.pk]))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_edit_any_entry(self):
        self.client.login(username='kristian', password='pw12345!')
        response = self.client.get(reverse('entry_edit', args=[self.alice_entry.pk]))
        self.assertEqual(response.status_code, 200)

    def test_billing_blocked_for_non_admin(self):
        self.client.login(username='alice', password='pw12345!')
        response = self.client.get(reverse('billing'))
        self.assertEqual(response.status_code, 403)

    def test_billing_allowed_for_admin(self):
        self.client.login(username='kristian', password='pw12345!')
        response = self.client.get(reverse('billing'))
        self.assertEqual(response.status_code, 200)
